import requests


def get_media(media_id, token):

    url = f"https://api.wistia.com/v1/stats/medias/{media_id}.json"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response.json()
