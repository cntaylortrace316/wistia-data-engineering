Wistia Analytics ETL Pipeline
Project Overview

This project implements an end-to-end data engineering pipeline that extracts video analytics data from the Wistia API, stores the results in structured datasets, and automates execution through GitHub Actions.

The pipeline is designed to:

Extract media metadata
Extract engagement metrics
Extract visitor-level data
Support incremental ingestion
Handle API pagination
Execute automatically through CI/CD
Generate structured datasets for analysis and reporting

Architecture
Wistia API 
  * Media Metadata Endpoint
  * Midia Stat Endpoint
  * Visitor Endpoint
Python ETL Pipeline
  * Pagination Logic
  * Incremental Ingestion Logic
  * Data Validation
CSV Storage Layer
  * media_metadata.csv
  * engagement_metrics.csv
  * visitor_data.csv
GitHub Actions
  * Automated Execution
  * Secret Management

Data Sources
Media Metadata 
  * Endpoint -
      * Get/modern/medias
  * Purpose:
      * Media ID
      * Hashed ID
      * Media Name
      * Duration
      * Created Date
      * Updated Date
      * Folder Information
Engagement Metrics
  * Endpoint
      * GET /v1/stats/medias/{media_id}.json
  * Purpose:
      * Load Count
      * Play Count
      * Play Rate
      * Watch Time
      * Engagement Rate
      * Visitor Count
Visitor Data
  * Endpoint
      * GET /modern/stats/visitors
  * Purpose
      * Visitor Activity
      * Device Information
      * Browser Information
      * Visitor Creation Date
      * Last Activity Date

Output Files
media_metadata.csv
  Snapshot table containing current media information. Full refresh each run
  Columns:
    * media_id
    * media_hashed_id
    * media_name
    * media_type
    * duration
    * created
    * updated
    *status
    * folder_name
engagement_metrics.csv
  Historical fact table containing engagement measurements over time. Append-only
  Columns:
    * extracted_at
    * media_id
    * load_count
    * play_count
    * play_rate
    * hours_watched
    * engagement
    * visitors
visitor_data.csv
  Visitor-level dataset containing user activity and device information. Incremental append
  Columns:
    * visitor_key
    * created_at
    * last_active_at
    * load_count
    * play_count
    * browser
    * browser_version
    * platform
    * mobile

Incremental Ingestion
  Pipeline stat is tracked using: last_run.json
  The pipline compares visitor timestamps against the previous execution timestamp and only loads newly created visitors

Pagination
  Pagination is implemented for:
    Media Metadata - Parameters: page, per_page
    Visitor Data - Parameters: page, per_page

CI/CD
Github Actions is used to automate execution.
  Workflow
    * .github/workflows/pipeline.yml
  Features:
    * Source control integration
    * Automated execution
    * Environment variable management
    * Secret management

Security
API tokens are not stored in source code. 
  GitHub Secret:
    * WISTIA_API_TOKEN
  Python retrieves the using
    * os.getenv("WISTIA_API_TOKEN")

Repository Structure
.github
  /workflows
    /pipeline.yml
ingestion
  /extract_media.py
tests
  /test_media_list.py
  /test_visitors.py  
README.md
requirments.txt
.gitingnore

Author
Corinne Taylor-Trace
  
