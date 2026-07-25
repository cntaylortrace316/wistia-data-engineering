import requests
import urllib3
import os
import csv
import json
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



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


def save_metrics_to_csv(stats, media_id, file_path="engagement_metrics.csv"):

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

    fieldnames = row.keys()

    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)



def get_last_run(file_path="last_run.json"):
    """
    Read last pipeline execution timestamp.
    """

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data["last_run"]

    except FileNotFoundError:
        return None


def update_last_run(file_path="last_run.json"):
    """
    Save current execution timestamp.
    """

    data = {
        "last_run": datetime.now().isoformat()
    }

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)




if __name__ == "__main__":

    last_run = get_last_run()

    print(f"Last Run: {last_run}")

    API_TOKEN = os.getenv("WISTIA_API_TOKEN")
    MEDIA_ID = "v08dlrgr7v"

    stats = get_media_stats(MEDIA_ID, API_TOKEN)

    print(f"Loads: {stats['load_count']:,}")
    print(f"Plays: {stats['play_count']:,}")

    save_metrics_to_csv(stats, MEDIA_ID)


    print("Metrics saved to engagement_metrics.csv")

    update_last_run()

    print("Updated last_run.json")
