import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # remove later


def get_media_stats(media_id, api_token):
    url = f"https://api.wistia.com/v1/stats/medias/{media_id}.json"

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    response = requests.get(
        url,
        headers=headers,
        verify=False  # remove later
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    API_TOKEN = "0323ade64e13f79821bdc0f2a9410d9ec3873aa9df01f8a4a54d4e0f3dd2e6b4"
    MEDIA_ID = "v08dlrgr7v"

    stats = get_media_stats(MEDIA_ID, API_TOKEN)

    print(stats)
