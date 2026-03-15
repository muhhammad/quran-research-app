from quran_letter_counter import count_letter_in_surah


def test_qaf_surah_50():

    plain, uthmani = count_letter_in_surah(50, "qaf")

    assert plain == 57
    assert uthmani == 57


def test_nun_surah_68():

    plain, uthmani = count_letter_in_surah(68, "nun")

    assert plain == 132