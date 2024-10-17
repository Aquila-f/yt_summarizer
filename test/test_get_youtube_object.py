from yt_summarizer.service.yt_helper import YTHelper


def test_get_youtube_object_valid_url():
    # Example valid YouTube URL
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = YTHelper.extract_info(url)

    assert result is not None, "Result should not be None for a valid URL"

    # Replace with expected values if known or mock the function for consistent results
    assert (
        result.title == "Rick Astley - Never Gonna Give You Up (Official Music Video)"
    ), "Unexpected title"


def test_get_youtube_object_invalid_url():
    # Invalid YouTube URL
    url = "https://www.youtube.com/watch?v=invalid"
    result = YTHelper.extract_info(url)

    # Assuming get_youtube_object returns None for invalid URLs
    assert result is None, "Result should be None for an invalid URL"


def test_get_youtube_object_empty_url():
    # Empty URL
    url = ""
    result = YTHelper.extract_info(url)

    # Assuming get_youtube_object returns None for empty URLs
    assert result is None, "Result should be None for an empty URL"


def test_get_youtube_object_non_youtube_url():
    # Non-YouTube URL
    url = "https://www.example.com"
    result = YTHelper.extract_info(url)

    # Assuming get_youtube_object returns None for non-YouTube URLs
    assert result is None, "Result should be None for a non-YouTube URL"
