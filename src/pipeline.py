from dagster import job, op, ScheduleDefinition, repository
import subprocess
import os

@op
def scrape_telegram_data():
    subprocess.run(["python", "src/scraper.py"])
    return "Scraped"

@op
def load_raw_to_postgres(context, scrape_result):
    subprocess.run(["python", "src/load_to_postgres.py"])
    return "Loaded"

@op
def run_dbt_transformations(context, load_result):
    os.chdir("medical_warehouse")
    subprocess.run(["dbt", "run"])
    subprocess.run(["dbt", "test"])
    os.chdir("..")
    return "Transformed"

@op
def run_yolo_enrichment(context, dbt_result):
    subprocess.run(["python", "src/yolo_detect.py"])
    # Assuming load_csv_to_db is called inside or separately
    subprocess.run(["python", "src/load_to_postgres.py"])  # Reuse for CSV load
    os.chdir("medical_warehouse")
    subprocess.run(["dbt", "run"])  # Re-run to build fct_image_detections
    os.chdir("..")
    return "Enriched"

@job
def medical_pipeline():
    scrape = scrape_telegram_data()
    load = load_raw_to_postgres(scrape)
    dbt = run_dbt_transformations(load)
    yolo = run_yolo_enrichment(dbt)

# Schedule daily at 00:00
daily_schedule = ScheduleDefinition(
    job=medical_pipeline,
    cron_schedule="0 0 * * *"
)

@repository
def medical_repo():
    return [medical_pipeline, daily_schedule]