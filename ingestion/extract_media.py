import requests
import urllib3
import os

API_TOKEN = os.getenv("WISTIA_API_TOKEN")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_media_stats(media_id, api_token):
    """
    Retrieve Wistia media statistics.

    Returns:
        dict: Media statistics from Wistia API.
    """

    url = f"https://api.wistia.com/v1/stats/medias/{media_id}.json"

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    response = requests.get(
        url,
        headers=headers,
        verify=False  # Remove later
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    API_TOKEN = os.getenv("WISTIA_API_TOKEN")
    MEDIA_ID = "v08dlrgr7v"

    stats = get_media_stats(MEDIA_ID, API_TOKEN)

    print(f"Loads: {stats['load_count']:,}")
    print(f"Plays: {stats['play_count']:,}")
    print(f"Play Rate: {stats['play_rate']:.2%}")
    print(f"Hours Watched: {stats['hours_watched']:,.2f}")
    print(f"Engagement: {stats['engagement']:.2%}")
    print(f"Visitors: {stats['visitors']:,}")
