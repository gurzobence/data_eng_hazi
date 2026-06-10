# Városi közbringa-használat és időjárás korrelációjának elemzése

**Készítette:** Gurzó Bence  
**Neptun-kód:** FO1YBI  
**E-mail:** gurzobence24@gmail.com  

## A projekt bemutatása
Ez a projekt egy teljes, end-to-end data engineering pipeline, amely Washington D.C. közbringa-hálózatának (Capital Bikeshare) utazási adatait veti össze a lokális historikus meteorológiai adatokkal. A pipeline célja, hogy bemutassa, hogyan befolyásolja a hőmérséklet és a csapadék a bérlések volumenét és a felhasználói szokásokat.

## Architektúra és Eszközök
A rendszer a modern adatinfrastruktúra (Modern Data Stack) elemeire épül:
* **Adatforrások:** Open-Meteo REST API (historikus JSON adatok) és Capital Bikeshare AWS S3 publikus bucket (CSV archívumok).
* **Infrastruktúra:** A teljes környezet konténerizált, a futtatást a Docker Compose biztosítja.
* **Orchestráció:** Az adatmozgatást és a feladatok idempotens ütemezését (DAG) az Apache Airflow vezérli.
* **Landing Zone (Bronze):** A nyers adatok egy S3-kompatibilis, lokálisan hosztolt MinIO objektumtárolóba landolnak.
* **Adattárház & OLAP motor:** Az adatbázis szerepét a DuckDB tölti be, amely képes közvetlenül, a hálózaton keresztül olvasni az S3-ban tárolt nyers fájlokat.
* **Transzformáció (ELT):** Az adatok tisztítását és a Kimball-féle csillag séma felépítését a dbt (Data Build Tool) végzi.

## Telepítési és Futtatási Útmutató

### 1. Előfeltételek
* Docker és Docker Compose telepítése a hoszt gépen.
* Git verziókövető rendszer megléte.

### 2. A projekt klónozása és indítása
Nyiss egy parancssort, és futtasd az alábbi parancsokat:
```bash
git clone <IDE_ILLESZD_A_GITHUB_REPO_LINKJED>
cd data_engineering_hazi
docker-compose up -d
```

### 3. A MinIO (Landing Zone) előkészítése
1. Nyisd meg a böngésződben a MinIO webes felületét: `http://localhost:9001`
2. Lépj be a hitelesítő adatokkal (**Username:** `minioadmin`, **Password:** `minioadmin`).
3. Hozz létre manuálisan egy új bucketet **`bronze`** néven. *(Ez a lépés kritikus az adatok fogadásához!)*

### 4. Az Airflow pipeline indítása
1. Nyisd meg az Airflow UI-t: `http://localhost:8080`
2. Lépj be az `admin` / `admin` adatokkal.
3. Keresd meg az `end_to_end_pipeline` nevű DAG-ot, és engedélyezd a bal oldali kapcsolóval (Unpause).
4. Indítsd el manuálisan a futtatást a jobb felső sarokban lévő "Trigger DAG" (Play) gombbal.
5. A folyamat párhuzamosan letölti a nyers fájlokat a MinIO-ba, majd a sikeresség után elindítja a dbt transzformációkat.

### 5. Adatkiszolgálás tesztelése (DBeaver)
A folyamat lefutása után a kész adattárház a `./data/warehouse.duckdb` útvonalon jön létre. Ha DBeaver klienst használsz, a lekérdezések futtatása előtt az alábbi SQL blokkal kell inicializálnod a MinIO elérést az S3-hoz:
```sql
INSTALL httpfs;
LOAD httpfs;
SET s3_endpoint='localhost:9000';
SET s3_access_key_id='minioadmin';
SET s3_secret_access_key='minioadmin';
SET s3_use_ssl=false;
SET s3_url_style='path';
```
