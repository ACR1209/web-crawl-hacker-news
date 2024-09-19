from fastapi.testclient import TestClient
from app.main import app
from app.models.story import Story

client = TestClient(app)

def test_refresh():
    """
        Refresh endpoint should refresh the data stored in memory.
        Test steps:
            1. Get /
            2. Get /refresh
            3. Get /
            4. Assert that the data in the response is not the same as it was before
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"data": None}

    response = client.get("/refresh")
    assert response.status_code == 200
    assert response.json() == {"message": "success"}

    refreshed_response = client.get("/")
    assert refreshed_response.status_code == 200
    assert refreshed_response.json() != {"data": None}

def test_read_root():
    """
        Read root endpoint should return the data stored in memory.
        Test steps:
            1. Get /
            2. Assert that the data in the response is not None
            3. Assert that the data in the response is a list
            4. Assert that the data in the response is a list of 30 stories
            5. Assert that the data in the response is a list of stories
    """
    response = client.get("/")
    assert response.status_code == 200
    res = response.json()
    assert "data" in res
    assert isinstance(res["data"], list)
    assert len(res["data"]) == 30
    for story in res["data"]:
        assert isinstance(story["rank"], int)
        assert isinstance(story["title"], str)
        assert isinstance(story["comments"], int)
        assert isinstance(story["points"], int)

