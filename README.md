# Városi közbringa-használat és időjárás korrelációjának elemzése 

**Készítette:** Gurzó Bence  
**Neptun-kód:** FO1YBI

## A projekt bemutatása
Ez a projekt egy teljes, end-to-end data engineering pipeline, amely egy városi közbringa-hálózat (Capital Bikeshare) utazási adatait veti össze lokális historikus időjárási adatokkal. A pipeline célja, hogy bemutassa, hogyan befolyásolja a hőmérséklet és a csapadék a bérlések számát és átlagos időtartamát. 

A pipeline batch feldolgozási móddal, havi ütemezéssel fut. A nyers adatokat egy Data Lake Bronze rétegébe tölti, majd dbt segítségével Kimball-féle csillag sémát épít belőlük.

## Architektúra és Eszközök
A rendszer az alábbi adatinfrastrukturális elemekre épül:
**Adatforrások:** Open-Meteo REST API (historikus JSON adatok) és Capital Bikeshare AWS S3 publikus bucket (CSV archívumok).
**Infrastruktúra:** A teljes környezet konténerizáltan, Docker Compose segítségével fut.
**Orchestration:** Az adatmozgatást és a feladatok ütemezését (DAG) az Apache Airflow végzi.
**Landing Zone (Bronze):** A nyers fájlok egy S3-kompatibilis, lokálisan futó MinIO objektumtárolóba kerülnek.
**Adattárház és Adatmodell:** Az adatok tárolásáért a DuckDB in-process OLAP motor felel. A modell egy 1 ténytáblából (`fact_rides`) és 3 dimenziótáblából (`dim_date`, `dim_station`, `dim_weather`) álló csillag séma.
**Transzformáció:** Az ELT folyamat transzformációs szakaszát a dbt (Data Build Tool) biztosítja.

## Futtatási és Telepítési Utasítások

### 1. Előfeltételek
* Docker és Docker Compose telepítése a hoszt gépen.
* Git verziókövető rendszer.

### 2. A projekt klónozása és indítása
Nyiss egy terminált, és futtasd az alábbi parancsokat:
```bash
git clone https://github.com/gurzobence/data_eng_hazi
cd data_engineering_hazi
docker-compose up -d
