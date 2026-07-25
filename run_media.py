from ingestion.extract_media import get_media

token = "YOUR_WISTIA_TOKEN"

media = get_media(
    "8hunphufxp",
    token
)

print(media)
