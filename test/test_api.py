from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():

    r = client.get("/")

    assert r.status_code == 200


def test_verse_endpoint():

    r = client.post("/verse", data={"surah":96,"ayah":1})

    assert r.status_code == 200


def test_letter_endpoint():

    r = client.post("/letter", data={"letter":"qaf","surah":50})

    assert r.status_code == 200


def test_word_endpoint():

    r = client.post("/word", data={"word":"الله"})

    assert r.status_code == 200