import json
import re
import sys


class QuranWordCounter:

    def __init__(self, quran_file):

        with open(quran_file, "r", encoding="utf-8") as f:
            raw_quran = json.load(f)

        self.quran = {}

        for surah, ayahs in raw_quran.items():

            cleaned_ayahs = []

            for i, ayah in enumerate(ayahs):

                normalized = self._normalize_arabic(ayah)

                # remove Bismillah prefix (except Surah 1)
                if i == 0 and surah != "1":
                    if normalized.startswith("بسم الله الرحمن الرحيم"):
                        normalized = normalized.replace("بسم الله الرحمن الرحيم", "").strip()

                cleaned_ayahs.append(normalized)

            self.quran[surah] = cleaned_ayahs


    def _clean_text(self, text):

        text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
        text = re.sub(r'[\u06D6-\u06ED]', '', text)
        text = text.replace("ٱ", "ا")
        text = text.replace("ـ", "")
        text = re.sub(r'\s+', ' ', text)

        return text.strip()


    def _normalize_arabic(self, text):

        text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
        text = re.sub(r'[\u06D6-\u06ED]', '', text)
        text = text.replace("ٱ", "ا")
        text = text.replace("ـ", "")
        text = re.sub(r'\s+', ' ', text)

        return text.strip()


    def _count_words(self, text):

        text = self._clean_text(text)

        words = text.split()

        # remove Bismillah
        if words[:4] == ["بسم", "الله", "الرحمن", "الرحيم"] or \
           words[:4] == ["بسم", "الله", "الرحمٰن", "الرحيم"]:
            words = words[4:]

        return len(words)


    def count_words_in_ayah(self, surah, ayah):

        text = self.quran[str(surah)][ayah - 1]
        return self._count_words(text)


    def count_words_range(self, surah, start_ayah, end_ayah):

        total = 0

        for ayah in self.quran[str(surah)][start_ayah-1:end_ayah]:
            total += self._count_words(ayah)

        return total


# -----------------------------
# CLI Helpers
# -----------------------------

def parse_verses(arg):

    verses = []

    parts = arg.split(",")

    for part in parts:

        if "-" in part:
            start, end = map(int, part.split("-"))
            verses.extend(range(start, end + 1))
        else:
            verses.append(int(part))

    return verses


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    if len(sys.argv) != 4:

        print("\nUsage:")
        print("python3 quran_word_counter.py <quran_json> <surah> <verse_list>")
        print("\nExamples:")
        print("python3 quran_word_counter.py quran.json 96 1-5")
        print("python3 quran_word_counter.py quran.json 50 1,3,5")
        print("python3 quran_word_counter.py quran.json 50 1,5-10\n")

        sys.exit()

    quran_file = sys.argv[1]
    surah = int(sys.argv[2])
    verses = parse_verses(sys.argv[3])

    counter = QuranWordCounter(quran_file)

    total = 0

    print("\nSelected verses:\n")

    for v in verses:

        count = counter.count_words_in_ayah(surah, v)

        print(f"{surah}:{v} -> {count} words")

        total += count

    print("\nTotal words:", total)