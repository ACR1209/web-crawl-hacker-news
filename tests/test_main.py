from fastapi.testclient import TestClient
from app.main import app, settings
from app.utils.words import count_words

settings.ENVIRONMENT= "test"

client = TestClient(app)

def test_refresh():
    """
        Refresh endpoint should refresh the data stored in memory.
        Test steps:
            1. Get /
            2. Get /refresh
            3. Get /
            4. Assert that the data in the response is the same or different in case it changed
    """
    response = client.get("/data")
    assert response.status_code == 200
    assert response.json() != {"data": None}

    response = client.get("/refresh")
    assert response.status_code == 200
    assert response.json() == {"message": "success"}


    refreshed_response = client.get("/data")
    assert refreshed_response.status_code == 200
    assert refreshed_response.json() != {"data": None}


def test_read_root():
    """
        Read root endpoint should return the data stored in memory.
        Test steps:
            1. Get /
            2. Assert that the response status code is 200
            3. Assert that the response is HTML
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

def test_order_by_comments():
    response = client.get("/data?order_by=comments")
    expected_ranks = [7, 21, 25, 30, 18, 17, 1, 13, 19, 15, 16, 26, 22, 20, 3, 11, 23, 2, 12, 24, 4, 5, 9, 27, 29, 10, 6, 8, 14, 28]

    for story, expected_rank in zip(response.json()["data"], expected_ranks):
        assert story["rank"] == expected_rank

def test_order_by_points():
    response = client.get("/data?order_by=points")
    expected_ranks = [7, 13, 21, 18, 25, 17, 22, 20, 30, 1, 19, 24, 16, 23, 12, 2, 5, 15, 3, 26, 4, 9, 29, 6, 10, 27, 11, 8, 14, 28]

    for story, expected_rank in zip(response.json()["data"], expected_ranks):
        assert story["rank"] == expected_rank

def test_order_by_rank():
    response = client.get("/data?order_by=rank")
    expected_ranks = [i for i in range(1, 31)]

    for story, expected_rank in zip(response.json()["data"], expected_ranks):
        assert story["rank"] == expected_rank

def test_order_by_other():
    response = client.get("/data?order_by=unknown")
    expected_ranks = [i for i in range(1, 31)]

    for story, expected_rank in zip(response.json()["data"], expected_ranks):
        assert story["rank"] == expected_rank

def test_min_word_count():
    response = client.get("/data?count_words_min=6")
    expected_ranks = [2, 3, 5, 6, 7, 9, 10, 11, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 30]

    for story, expected_rank in zip(response.json()["data"], expected_ranks):
        assert story["rank"] == expected_rank

def test_max_word_count():
    response = client.get("/data?count_words_max=5")
    expected_ranks = [1, 4, 8, 12, 14, 15, 26, 29]

    for story, expected_rank in zip(response.json()["data"], expected_ranks):
        assert story["rank"] == expected_rank
    
def test_mixed_max_and_min_count():
    response = client.get("/data?count_words_max=1&count_words_min=5")
    expected_ranks = [1, 4, 8, 12, 14, 15, 26, 29]

    for story, expected_rank in zip(response.json()["data"], expected_ranks):
        assert story["rank"] == expected_rank

def test_max_and_min_count():
    response = client.get("/data?count_words_min=1&count_words_max=5")
    expected_ranks = [1, 4, 8, 12, 14, 15, 26, 29]

    for story, expected_rank in zip(response.json()["data"], expected_ranks):
        assert story["rank"] == expected_rank


def test_word_counter():
    tests = [
        {"word": "This is - a self-explained example", "count": 5},
        {"word": "Simple test", "count": 2},
        {"word": "Trailing spaces    ", "count": 2},
        {"word": "Leading spaces", "count": 2},
        {"word": "Multiple    spaces between words", "count": 4},
        {"word": "Word with punctuation, like commas, periods.", "count": 6},
        {"word": "Hyphenated-word should count as two words", "count": 6},
        {"word": "1234 numbers shouldn't affect counting", "count": 5},
        {"word": "Special characters #@$%^&* should be ignored", "count": 5},
        {"word": "Newline\ncharacters should count properly", "count": 5},
        {"word": "Tab\tseparation should count as a space", "count": 7},
        {"word": "", "count": 0},  # Empty string
        {"word": "SingleWord", "count": 1},  # One word with no spaces
        {"word": "Single character a", "count": 3},
        {"word": "   ", "count": 0},  # String with only spaces
        {"word": "dash-separated-words shouldn't be split", "count": 4},
        {"word": "sentence.with.punctuation", "count": 1},
        {"word": "Quotes 'single' and \"double\" are words", "count": 6},
        {"word": "Ellipsis...should count properly", "count": 3},
        {"word": "Combining-different things-like.hyphens and periods.", "count": 4},
        {"word": "Handle_unicode_Ω_γ_φ characters", "count": 2} 
    ]

    for test_case in tests:
        assert count_words(test_case["word"]) == test_case["count"]
