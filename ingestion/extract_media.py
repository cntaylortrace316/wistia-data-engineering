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

    all_media = []

    page = 1
    per_page = 100

    while True:

        url = "https://api.wistia.com/modern/medias"

        headers = {
            "Authorization": f"Bearer {api_token}",
            "accept": "application/json",
            "X-Wistia-API-Version": "2026-05"
        }

        params = {
            "page": page,
            "per_page": per_page
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            verify=False
        )

        response.raise_for_status()

        media_page = response.json()

        print(f"Page {page}: {len(media_page)} records")

        if len(media_page) == 0:
            break

        all_media.extend(media_page)

        if len(media_page) < per_page:
            break

        page += 1

    return all_media

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
    Save Wistia media metadata snapshot.
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

    return len(media_list)
            
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
        
def get_visitor_list(api_token):

    all_visitors = []

    page = 1
    per_page = 100

    while True:

        url = "https://api.wistia.com/modern/stats/visitors"

        headers = {
            "Authorization": f"Bearer {api_token}",
            "accept": "application/json",
            "X-Wistia-API-Version": "2026-05"
        }

        params = {
            "page": page,
            "per_page": per_page
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            verify=False
        )

        response.raise_for_status()

        visitor_page = response.json()

        print(f"Page {page}: {len(visitor_page)} visitors")

        if len(visitor_page) == 0:
            break

        all_visitors.extend(visitor_page)

        print(f"Total visitors collected: {len(all_visitors)}")
        print(f"Current page variable: {page}")

        if len(visitor_page) < per_page:
            break

        # Stop after page 5 for testing
        if page >= 5:
            print("Stopping after 5 pages for testing")
            break

        page += 1

    return all_visitors   
  
def save_visitor_data(
        visitor_list,
        file_path="visitor_data.csv"):
    """
    Save visitor-level data.
    """

    fieldnames = [
        "extracted_at",
        "visitor_key",
        "created_at",
        "last_active_at",
        "last_event_key",
        "load_count",
        "play_count",
        "visitor_name",
        "visitor_email",
        "org_name",
        "org_title",
        "browser",
        "browser_version",
        "platform",
        "mobile"
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

        for visitor in visitor_list:

            identity = visitor.get(
                "visitor_identity", {}
            )

            org = identity.get(
                "org", {}
            )

            user_agent = visitor.get(
                "user_agent_details", {}
            )

            row = {
                "extracted_at": datetime.now().isoformat(),
                "visitor_key": visitor.get("visitor_key"),
                "created_at": visitor.get("created_at"),
                "last_active_at": visitor.get("last_active_at"),
                "last_event_key": visitor.get("last_event_key"),
                "load_count": visitor.get("load_count"),
                "play_count": visitor.get("play_count"),

                "visitor_name": identity.get("name"),
                "visitor_email": identity.get("email"),

                "org_name": org.get("name"),
                "org_title": org.get("title"),

                "browser": user_agent.get("browser"),
                "browser_version": user_agent.get("browser_version"),
                "platform": user_agent.get("platform"),
                "mobile": user_agent.get("mobile")
            }

            writer.writerow(row)

    return len(visitor_list)  
        
# MAIN SECTION

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
    records_saved = save_media_metadata(
        media_list
    )

    print(
        f"Updated media_metadata.csv "
        f"({records_saved} records)"
    )

# VISITOR DATA

    visitor_list = get_visitor_list(
        API_TOKEN
    )

    records_saved = save_visitor_data(
        visitor_list
    )

    print(
        f"Updated visitor_data.csv "
        f"({records_saved} records)"
    )
        
    # STORE LAST RUN
    update_last_run()

    print("Updated last_run.json")
