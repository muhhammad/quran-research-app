import re
from quran_letter_counter import count_letter_in_surah
from quran_word_counter import QuranWordCounter

counter = QuranWordCounter("quran.json")


def verse_analysis(surah, ayah):

    text = counter.quran[str(surah)][ayah-1]

    words = text.split()
    letters = re.findall(r"[ء-ي]", text)

    return {
        "text": text,
        "words": len(words),
        "letters": len(letters)
    }


def letter_analysis(letter, surah):

    plain, uthmani = count_letter_in_surah(surah, letter)

    return {
        "plain": plain,
        "uthmani": uthmani,
        "plain_19": plain % 19 == 0,
        "uthmani_19": uthmani % 19 == 0
    }


def normalize_arabic(text):

    # remove diacritics
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)

    # remove Quran annotation marks
    text = re.sub(r'[\u06D6-\u06ED]', '', text)

    # normalize hamzat-wasl
    text = text.replace("ٱ", "ا")

    # remove tatweel
    text = text.replace("ـ", "")

    return text


def word_search(word):

    results = []
    total = 0

    normalized_word = normalize_arabic(word)

    pattern = re.compile(
        rf'(?<![\u0621-\u064A]){re.escape(normalized_word)}(?![\u0621-\u064A])'
    )

    for surah, ayahs in counter.quran.items():

        for i, ayah in enumerate(ayahs, start=1):

            normalized_ayah = normalize_arabic(ayah)

            matches = pattern.findall(normalized_ayah)

            if matches:

                count = len(matches)

                results.append(f"{surah}:{i} ({count}) {ayah}")

                total += count

    return results, total


def muqattaat_analysis():

    muqattaat = {
        2:"الم",3:"الم",7:"المص",10:"الر",11:"الر",12:"الر",13:"المر",
        14:"الر",15:"الر",19:"كهيعص",20:"طه",26:"طسم",27:"طس",
        28:"طسم",29:"الم",30:"الم",31:"الم",32:"الم",36:"يس",
        38:"ص",40:"حم",41:"حم",42:"حم عسق",43:"حم",44:"حم",
        45:"حم",46:"حم",50:"ق",68:"ن"
    }

    results = []

    for surah, letters in muqattaat.items():

        letters_list = list(letters.replace(" ", ""))

        counts = {}

        for l in letters_list:

            # find English name for letter
            from quran_letter_counter import letter_map

            name = None
            for k,v in letter_map.items():
                if v == l:
                    name = k

            if name:

                plain, uthmani = count_letter_in_surah(surah, name)

                counts[name] = {
                    "plain": plain,
                    "uthmani": uthmani,
                    "plain_19": plain % 19 == 0,
                    "uthmani_19": uthmani % 19 == 0
                }

        results.append({
            "surah": surah,
            "letters": letters,
            "counts": counts
        })

    return results