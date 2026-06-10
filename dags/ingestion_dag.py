from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import requests
import boto3
import json
import zipfile
import io

# Konstansok
MINIO_ENDPOINT = 'http://minio:9000'
MINIO_ACCESS_KEY = 'minioadmin'
MINIO_SECRET_KEY = 'minioadmin'
BRONZE_BUCKET = 'bronze'

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY
    )

def download_weather_data(**kwargs):
    start_date = kwargs['data_interval_start'].strftime('%Y-%m-%d')
    end_date = kwargs['data_interval_end'].strftime('%Y-%m-%d')
    run_month = kwargs['data_interval_start'].strftime('%Y%m')

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 38.907,
        "longitude": -77.036,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone": "America/New_York"
    }
    
    print(f"Időjárás adatok lekérése a {start_date} - {end_date} időszakra...")
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    file_name = f"weather_data_{run_month}.json"
    s3_client = get_s3_client()

    s3_client.put_object(
        Bucket=BRONZE_BUCKET,
        Key=f"weather/{file_name}",
        Body=json.dumps(data)
    )
    print(f"Sikeresen feltöltve: weather/{file_name}")

def download_bikeshare_data(**kwargs):
    run_month = kwargs['data_interval_start'].strftime('%Y%m')
    url = f"https://s3.amazonaws.com/capitalbikeshare-data/{run_month}-capitalbikeshare-tripdata.zip"
    
    print(f"Bikeshare ZIP letöltése innen: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"Nincs adat erre a hónapra: {run_month}. (404 Not Found)")
            return
        else:
            raise e
    
    s3_client = get_s3_client()
    
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        csv_files = [f for f in z.namelist() if f.endswith('.csv') and not f.startswith('__MACOSX')]
        
        for file_name in csv_files:
            standard_name = f"bikeshare_rides_{run_month}.csv"
            print(f"Feldolgozás és feltöltés: bikeshare/{standard_name}")
            csv_content = z.read(file_name)
            
            s3_client.put_object(
                Bucket=BRONZE_BUCKET,
                Key=f"bikeshare/{standard_name}",
                Body=csv_content
            )
    print("Bikeshare adatok feltöltése sikeres!")

# --- DAG Definiálása ---
with DAG(
    'end_to_end_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@monthly',
    catchup=False,
    description='Nyers adatok letöltése, majd dbt transzformáció',
    tags=['ELT', 'bronze', 'silver', 'gold']
) as dag:

    # 1. Nyers adat letöltési feladatok
    fetch_weather_task = PythonOperator(
        task_id='fetch_open_meteo_data',
        python_callable=download_weather_data
    )

    fetch_bikeshare_task = PythonOperator(
        task_id='fetch_bikeshare_data',
        python_callable=download_bikeshare_data
    )

    # 2. dbt transzformációs feladat
    run_dbt_models = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /opt/airflow/dbt && dbt run',
    )

    # 3. Függőségek (Dependencies) beállítása
    # A dbt run csak azután indulhat el, hogy a két letöltés sikeresen (párhuzamosan) befejeződött
    [fetch_weather_task, fetch_bikeshare_task] >> run_dbt_models