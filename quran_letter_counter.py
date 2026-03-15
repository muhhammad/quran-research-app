import re
import unicodedata

letter_map={
"alif":"ا","ba":"ب","ta":"ت","tha":"ث","jeem":"ج","ha":"ح","kha":"خ",
"dal":"د","dhal":"ذ","ra":"ر","zay":"ز","seen":"س","sheen":"ش",
"sad":"ص","dad":"ض","ta2":"ط","za":"ظ","ain":"ع","ghain":"غ",
"fa":"ف","qaf":"ق","kaf":"ك","lam":"ل","meem":"م","nun":"ن",
"ha2":"ه","waw":"و","ya":"ي"
}

ayah_counts=[
7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,
110,98,135,112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,
83,182,88,75,85,54,53,89,59,37,35,38,29,18,45,60,49,62,55,
78,96,29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,
56,40,31,50,40,46,42,29,19,36,25,22,17,19,26,30,20,15,21,
11,8,8,19,5,8,8,11,11,8,3,9,5,4,7,3,6,3,5,4,5,6
]

muqattaat={
2:"الم",3:"الم",7:"المص",10:"الر",11:"الر",12:"الر",13:"المر",
14:"الر",15:"الر",19:"كهيعص",20:"طه",26:"طسم",27:"طس",
28:"طسم",29:"الم",30:"الم",31:"الم",32:"الم",36:"يس",
38:"ص",40:"حم",41:"حم",42:"حم",43:"حم",44:"حم",45:"حم",
46:"حم",50:"ق",68:"ن"
}

diacritics=re.compile(r'[ًٌٍَُِّْـٰ]')


def normalize(text):
    text=unicodedata.normalize("NFKD",text)
    text=re.sub(diacritics,"",text)
    text=text.replace(" ","").strip()
    return text


def _count_letters(file,surah,letter):

    start=sum(ayah_counts[:surah-1])
    end=start+ayah_counts[surah-1]

    count=0

    with open(file,encoding="utf-8") as f:
        lines=f.readlines()

    surah_lines=lines[start:end]

    for line in surah_lines:
        text=normalize(line)
        count+=sum(1 for c in text if c==letter)

    if surah in muqattaat:
        count+=muqattaat[surah].count(letter)

    return count


def count_letter_in_surah(surah, letter_name):

    letter_name = letter_name.lower()

    if letter_name not in letter_map:
        raise ValueError("Unknown letter")

    letter = letter_map[letter_name]

    plain = _count_letters("quran-simple-plain.txt", surah, letter)
    uthmani = _count_letters("quran-uthmani.txt", surah, letter)

    # Exclude Muqattaʿat opening letter
    if surah in muqattaat:
        opening = muqattaat[surah]
        if letter in opening:
            plain -= opening.count(letter)
            uthmani -= opening.count(letter)

    return plain, uthmani


def count_all_letters_in_verses(surah, verses):

    start = sum(ayah_counts[:surah-1])

    letter_counts_plain = {}
    letter_counts_uthmani = {}

    with open("quran-simple-plain.txt", encoding="utf-8") as f:
        lines = f.readlines()

    for v in verses:
        text = normalize(lines[start + v - 1])

        for c in text:
            if c.isalpha():
                letter_counts_plain[c] = letter_counts_plain.get(c, 0) + 1


    with open("quran-uthmani.txt", encoding="utf-8") as f:
        lines = f.readlines()

    for v in verses:
        text = normalize(lines[start + v - 1])

        for c in text:
            if c.isalpha():
                letter_counts_uthmani[c] = letter_counts_uthmani.get(c, 0) + 1


    return letter_counts_plain, letter_counts_uthmani