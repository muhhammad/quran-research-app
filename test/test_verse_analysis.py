from app.analysis import verse_analysis


def test_surah_96_verse_1():

    result = verse_analysis(96,1)

    assert result["words"] == 5
    assert result["letters"] == 18