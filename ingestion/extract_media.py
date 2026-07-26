import requests
import urllib3
import os
import csv
import json
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# WISTIA STATS API

def get_media_stats(media_id, api_token):
    url = f"https://api.wistia.com/v1/stats/medias/{media_id}.json"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(
        url,
        headers=headers,
        verify=False
    )
    response.raise_for_status()
    return response.json()

# WISTIA MEDIA LIST API
def get_media_list(api_token):
    url = "https://api.wistia.com/modern/medias"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "accept": "application/json",
        "X-Wistia-API-Version": "2026-05"
    }
    response = requests.get(
        url,
        headers=headers,
        verify=False
    )
    response.raise_for_status()
    return response.json()

# ENGAGEMENT METRICS CSV

def save_metrics_to_csv(
        stats,
        media_id,
        file_path="engagement_metrics.csv"):
    row = {
        "extracted_at": datetime.now().isoformat(),
        "media_id": media_id,
        "load_count": stats.get("load_count"),
        "play_count": stats.get("play_count"),
        "play_rate": stats.get("play_rate"),
        "hours_watched": stats.get("hours_watched"),
        "engagement": stats.get("engagement"),
        "visitors": stats.get("visitors")
    }
    file_exists = os.path.exists(file_path)
    with open(
            file_path,
            mode="a",
            newline="",
            encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=row.keys()
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
                
# MEDIA METADATA CSV

def save_media_metadata(
        media_list,
        file_path="media_metadata.csv"):
    """
    Save Wistia media metadata.
    """
    fieldnames = [
        "extracted_at",
        "media_id",
        "media_hashed_id",
        "media_name",
        "media_type",
        "duration",
        "created",
        "updated",
        "status",
        "archived",
        "folder_id",
        "folder_hashed_id",
        "folder_name"
    ]
    with open(
            file_path,
            mode="w",
            newline="",
            encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )
        writer.writeheader()
        for media in media_list:
            folder = media.get("folder", {})
            row = {
                "extracted_at": datetime.now().isoformat(),
                "media_id": media.get("id"),
                "media_hashed_id": media.get("hashed_id"),
                "media_name": media.get("name"),
                "media_type": media.get("type"),
                "duration": media.get("duration"),
                "created": media.get("created"),
                "updated": media.get("updated"),
                "status": media.get("status"),
                "archived": media.get("archived"),
                "folder_id": folder.get("id"),
                "folder_hashed_id": folder.get("hashed_id"),
                "folder_name": folder.get("name")
            }
            writer.writerow(row)
            
# INCREMENTAL INGESTION

def get_last_run(file_path="last_run.json"):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data["last_run"]
    except FileNotFoundError:
        return None
        
def update_last_run(file_path="last_run.json"):
    data = {
        "last_run": datetime.now().isoformat()
    }
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
        
# MAIN TEST

if __name__ == "__main__":
    last_run = get_last_run()
    print(f"Last Run: {last_run}")
    API_TOKEN = os.getenv("WISTIA_API_TOKEN")
    MEDIA_ID = "v08dlrgr7v"

    # UPDATE STATS
    stats = get_media_stats(
        MEDIA_ID,
        API_TOKEN
    )
    save_metrics_to_csv(
        stats,
        MEDIA_ID
    )
    print("Updated engagement_metrics.csv")


    # STORE METADATA IN MEDIA_METADATA.CSV

    media_list = get_media_list(
        API_TOKEN
    )
    save_media_metadata(
        media_list
    )
    print(
        f"Updated media_metadata.csv "
        f"({len(media_list)} records)"
    )
    
    # STORE LAST RUN
    update_last_run()

    print("Updated last_run.json")
