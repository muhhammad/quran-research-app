from app.analysis import word_search


def test_word_allah_exists():

    results, total = word_search("الله")

    assert total > 0