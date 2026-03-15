from app.analysis import muqattaat_analysis


def test_muqattaat_surah_50():

    data = muqattaat_analysis()

    s50 = next(x for x in data if x["surah"] == 50)

    assert s50["counts"]["qaf"]["plain"] == 57