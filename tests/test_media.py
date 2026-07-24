from ingestion.extract_media import get_media

def test_media_id_exists():

    media = get_media()

    assert "media_id" in media


def test_media_title_exists():

    media = get_media()

    assert "title" in media


def test_records_returned():

    media = get_media()

    assert media is not None
