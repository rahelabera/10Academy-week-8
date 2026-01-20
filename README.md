# 10 Academy: Artificial Intelligence Mastery  
**Week 8 Challenge Document**  
**Shipping a Data Product: From Raw Telegram Data to an Analytical API**  

An end-to-end data pipeline for Telegram, leveraging dbt for transformation, Dagster for orchestration, and YOLOv8 for data enrichment.

## Overview

### Business Need

You are a Data Engineer at **Kara Solutions**, a leading data science consultancy in Ethiopia.  
Your team has been tasked with building a robust data platform that generates actionable insights about Ethiopian medical businesses, using data scraped from public Telegram channels.

A well-designed data platform significantly enhances data analysis. To achieve this, you will build an end-to-end pipeline that answers key business questions such as:

- What are the top 10 most frequently mentioned medical products or drugs across all channels?
- How does the price or availability of a specific product vary across different channels?
- Which channels have the most visual content (e.g., images of pills vs. creams)?
- What are the daily and weekly trends in posting volume for health-related topics?

To answer these questions, you will implement a modern **ELT** (Extract, Load, Transform) framework. Raw data will be extracted from Telegram and loaded into a "Data Lake" storage zone. From there, it will be loaded into a PostgreSQL database, which will serve as your data warehouse. The crucial transformation step will happen inside the warehouse using **dbt**, where you will clean the data and remodel it into a dimensional star schema optimized for analytical queries. This layered approach ensures your data is reliable, scalable, and ready for analysis.

This project involves scraping, data modeling, object detection with YOLO to enrich the data, and exposing the final insights through an analytical API.

**Your job is to build a data product that does the following:**

- Develop a reproducible project environment and secure pipeline.
- Develop a data scraping and collection pipeline to populate a raw data lake.
- Design and implement a dimensional data model (star schema) in a PostgreSQL data warehouse.
- Develop a data cleaning and transformation pipeline using dbt.
- Enrich the data using object detection on images with YOLO.
- Expose the final, cleaned data through an analytical API using FastAPI.

## Data and Features

You will be building a **data warehouse** for this project. The data comes from public Telegram channels that sell medical and pharmaceutical products in Ethiopia.

### Telegram Channels to Scrape:

- CheMed Telegram Channel - Medical products
- Lobelia Cosmetics - Cosmetics and health products
- Tikvah Pharma - Pharmaceuticals
- Additional channels from https://et.tgstat.com/medicine

### Data Fields You Will Collect:

- `message_id` - Unique identifier for each message
- `channel_name` - Name of the Telegram channel
- `message_date` - Timestamp of the message
- `message_text` - Full text content (product names, prices, descriptions)
- `has_media` - Whether the message contains media
- `image_path` - Path to downloaded image (if applicable)
- `views` - Number of views on the message
- `forwards` - Number of times the message was forwarded

### Communication & Support

- Slack channel: #all-week8
- Office hours: Mon–Fri, 08:00–15:00 UTC

## Learning Outcomes

### Skills:

- Telegram API data extraction using Telethon
- Data Modeling: Designing and implementing a Star Schema
- ELT Pipeline Development: Building layered data pipelines (Raw → Staging → Marts)
- Infrastructure as Code (IaC) and environment management using Docker and requirements.txt
- Data Transformation at scale using dbt (Data Build Tool)
- Data Enrichment using Object Detection (YOLO)
- Analytical API Development with FastAPI
- Data Pipeline Orchestration with Dagster
- Testing and validation of data systems
- Managing credentials and secrets using environment variables

### Knowledge:

- Principles of modern ELT vs. ETL architectures
- Layered data architecture (Data Lake, Staging, Data Marts)
- Best practices in data cleaning, validation, and transformation
- Structuring data for efficient analytical queries (Dimensional Modeling)
- Integrating unstructured data (like image detection results) into a structured warehouse
- Best practices for deploying and maintaining reproducible data pipelines

### Communication:

- Documenting data architecture and modeling decisions
- Reporting on project outcomes and technical challenges

### Team

**Tutors:**

- Kerod
- Mahbubah
- Filimon
- Smegnsh

### Key Dates

- Challenge Introduction – 10:30 AM UTC on Wednesday, 14 Jan 2026
- Interim Submission – 8:00 PM UTC on Sunday, 18 Jan 2026
- Final Submission – 8:00 PM UTC on Tuesday, 20 Jan 2026

## Deliverables

### Project Structure

medical-telegram-warehouse/
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── unittests.yml
├── .env               # Secrets (API keys, DB passwords) - DO NOT COMMIT
├── .gitignore
├── docker-compose.yml  # Container orchestration
├── Dockerfile          # Python environment
├── requirements.txt
├── README.md
├── data/
├── medical_warehouse/            # dbt project
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── tests/
├── src/
├── api/
│   ├── init.py
│   ├── main.py                   # FastAPI application
│   ├── database.py               # Database connection
│   └── schemas.py                # Pydantic models
├── notebooks/
│   ├── init.py
├── tests/
│   └── init.py
└── scripts/

## Task 1 - Data Scraping and Collection (Extract & Load)

**Objective:** Build a data scraping pipeline that extracts messages and images from Telegram channels and stores them in a raw data lake.

**Instructions:**

1. Set Up Telegram API Access
   - Register your application at my.telegram.org to get API credentials.
   - Install and configure the Telethon library.

2. Telegram Scraping:
   - Utilize the Telegram API or write custom scripts to extract data from public Telegram channels relevant to Ethiopian medical businesses. Use the following channels:
     - Chemed Telegram Channel
     - https://t.me/lobelia4cosmetics
     - https://t.me/tikvahpharma
     - And many more from https://et.tgstat.com/medicine
   - For each message, extract:
     - Message ID, date, text content
     - View count, forward count
     - Media information (if present)

3. Download Images
   - When a message contains a photo, download it
   - Store images in an organized folder structure: `data/raw/images/{channel_name}/{message_id}.jpg`

4. Populate the Data Lake
   - Store raw scraped data as JSON files
   - Use a partitioned directory structure: `data/raw/telegram_messages/YYYY-MM-DD/channel_name.json`
   - Preserve the original data structure from the API

5. Implement Logging
   - Log which channels and dates have been scraped
   - Capture any errors (e.g., rate limiting, network issues)
   - Store logs in a `logs/` directory

**Deliverables:**
- A working scraper script (`src/scraper.py`)
- Raw JSON files in the data lake structure
- Downloaded images organized by channel
- Log files showing scraping activity

## Task 2 - Data Modeling and Transformation (Transform)

**Objective:** Transform raw, messy data into a clean, structured data warehouse using dbt and dimensional modeling.

**Instructions:**

1. Load Raw Data to PostgreSQL
   - Write a Python script that:
     - Reads JSON files from your data lake
     - Loads them into a raw schema in PostgreSQL
     - Creates a table `raw.telegram_messages` with all scraped fields

2. Initialize dbt Project
    - pip install dbt-postgres
    - dbt init medical_warehouse
    - Configure `profiles.yml` to connect to your PostgreSQL database
- Set up the project structure

3. Create Staging Models: Staging models clean and standardize raw data. Create in `models/staging/`:
- Cast data types appropriately (dates, integers, etc.)
- Rename columns to consistent naming conventions
- Remove or filter invalid records (empty messages, nulls)
- Add calculated fields (message_length, has_image flag)
- You should have one staging model per raw source (e.g., `stg_telegram_messages.sql`).

4. Design and Implement Star Schema: Create a dimensional model with the following tables in `models/marts/`:
- **Dimension Tables:**
  - `dim_channels`: channel_key (surrogate key), channel_name, channel_type (Pharmaceutical, Cosmetics, Medical), first_post_date, last_post_date, total_posts, avg_views
  - `dim_dates`: date_key, full_date, day_of_week, day_name, week_of_year, month, month_name, quarter, year, is_weekend
- **Fact Table:**
  - `fct_messages`: message_id, channel_key (FK), date_key (FK), message_text, message_length, view_count, forward_count, has_image

5. Implement dbt Tests: In `models/marts/schema.yml`, add:
- unique and not_null tests to validate primary keys and critical columns
- relationships tests on foreign keys

6. Create a Custom Data Test: Write at least one custom test in `tests/` directory. For example:
- `assert_no_future_messages.sql`: Ensure no messages have future dates
- `assert_positive_views.sql`: Ensure view counts are non-negative
- These tests (SQL query) must return 0 rows to pass.

7. Generate Documentation
    - dbt docs generate
    - dbt docs serve
    - Add descriptions to all models and columns in `schema.yml`

**Deliverables:**
- Complete dbt project with staging and mart models
- All dbt tests passing (`dbt test` shows no failures)
- Generated dbt documentation
- A section in your report explaining your star schema design decisions

## Task 3 - Data Enrichment with Object Detection (YOLO)

**Objective:** Use computer vision to analyze images and integrate the findings into your data warehouse.

**Instructions:**

1. Set Up YOLO Environment
    - pip install ultralytics
    - Use the YOLOv8 nano model (`yolov8n.pt`) for efficiency on standard laptops

2. Implement Object Detection Script  
Create `src/yolo_detect.py` that:
- Scans for images downloaded in Task 1
- Runs YOLOv8 detection on each image
- Records detected objects with confidence scores
- Saves results to a CSV file

3. Create Classification Scheme  
Based on detected objects, categorize each image:
- promotional: Contains person + product (someone showing/holding item)
- product_display: Contains bottle/container, no person
- lifestyle: Contains person, no product
- other: Neither detected

4. Integrate with Data Warehouse  
Create a new dbt model `models/marts/fct_image_detections.sql`:
- Load YOLO results into PostgreSQL
- Join with `fct_messages` on message_id
- Include: message_id, channel_key, date_key, detected_class, confidence_score, image_category

5. Analyze Results  
In your report, answer:
- Do "promotional" posts (with people) get more views than "product_display" posts?
- Which channels use more visual content?
- What are the limitations of using pre-trained models for domain-specific tasks?

**Deliverables:**
- Object detection script (`src/yolo_detect.py`)
- Detection results CSV file
- `fct_image_detections` dbt model integrated into warehouse
- Analysis of image content patterns in your report

## Task 4 - Build an Analytical API

**Objective:** Expose your data warehouse through a REST API that answers business questions.

**Instructions:**

1. Set Up FastAPI Project
    - pip install fastapi uvicorn
    - Create the API structure in the `api/` directory
- Set up database connection using SQLAlchemy

2. Implement Analytical Endpoints: Create endpoints that query your dbt models (data marts):
- **Endpoint 1:** Top Products: Returns the most frequently mentioned terms/products across all channels.  
  `GET /api/reports/top-products?limit=10`
- **Endpoint 2:** Channel Activity: Returns posting activity and trends for a specific channel.  
  `GET /api/channels/{channel_name}/activity`
- **Endpoint 3:** Message Search: Searches for messages containing a specific keyword.  
  `GET /api/search/messages?query=paracetamol&limit=20`
- **Endpoint 4:** Visual Content Stats: Returns statistics about image usage across channels.  
  `GET /api/reports/visual-content`

3. Add Data Validation
- Use Pydantic models in `api/schemas.py` to define request/response structures
- Add proper error handling and HTTP status codes

4. Document the API
- FastAPI automatically generates OpenAPI documentation
- Access at `/docs` when the server is running
- Add descriptions to all endpoints and parameters

**Deliverables:**
- Working FastAPI application (`api/main.py`)
- At least 4 analytical endpoints
- Pydantic schemas for request/response validation
- Screenshots of API documentation and example responses

## Task 5 - Pipeline Orchestration

**Objective:** Automate your entire pipeline using an orchestration tool.

**Instructions:**

1. Install Dagster
    - pip install dagster dagster-webserver
    
2. Define Pipeline as a Dagster Job: Convert your pipeline into Dagster "ops" (operations):
- `scrape_telegram_data`: Run the scraper
- `load_raw_to_postgres`: Load JSON to database
- `run_dbt_transformations`: Execute dbt models
- `run_yolo_enrichment`: Run object detection

3. Create the Job Graph
- Define dependencies between ops
- Ensure proper execution order

4. Launch and Test
    - dagster dev -f pipeline.py
    - Access the Dagster UI at http://localhost:3000
- Run the pipeline manually
- Monitor execution and logs

5. Add Scheduling
- Configure the pipeline to run daily
- Set up alerts for failures