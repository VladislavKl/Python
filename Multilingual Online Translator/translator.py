
import sys
import requests

from bs4 import BeautifulSoup

LANGUAGES = {
    1: "Arabic",
    2: "German",
    3: "English",
    4: "Spanish",
    5: "French",
    6: "Hebrew",
    7: "Japanese",
    8: "Dutch",
    9: "Polish",
    10: "Portuguese",
    11: "Romanian",
    12: "Russian",
    13: "Turkish"
}


def translate(language, language2, word, file):
    try:
        r = requests.get('https://context.reverso.net/translation/' +
                     f"{LANGUAGES[language].lower()}-{LANGUAGES[language2].lower()}/"
                     + word,
                     headers={'User-Agent': 'Mozilla/5.0'})
    except Exception:
        print(f"Sorry, the program doesn't support {language2 if type(language2) is str else language}")

    else:
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            transls = soup.find_all("a", ["ltr", "dict"])
            res = []
            for t in transls:
                res.append(t.text.strip())
            res = res[:5]
            # print(f"\n{LANGUAGES[language2]} Translations:")
            file.write(f"\n{LANGUAGES[language2]} Translations:\n")
            for t in res:
                # print(t)
                file.write(t+"\n")
            exampls = soup.find_all("div", {"class": {"src ltr", "trg ltr"}})
            res2 = []
            for t in exampls:
                res2.append(t.text.strip())
            # print(f"\n{LANGUAGES[language2]} Examples:")
            file.write(f"\n{LANGUAGES[language2]} Examples:\n")
            for t in range(0, 10, 2):
                # print(res2[t] + ":")
                # print(res2[t + 1] + "\n")
                file.write(res2[t] + ":\n")
                file.write(res2[t + 1] + "\n\n")
        else:
            print(f'Sorry, unable to find {word}')


print(
    """Hello, you're welcome to the translator. Translator supports: 
1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian
12. Russian
13. Turkish
""")


if len(sys.argv) > 1:
    language = sys.argv[1]
    language2 = sys.argv[2]
    word = sys.argv[3]
else:
    language = int(input("Type the number of your language: "))
    language2 = int(input("Type the number of a language you want to translate to or '0' to translate to all LANGUAGES: "))
    word = input('Type the word you want to translate: ')

for num, lang in LANGUAGES.items():
    if type(language) is str and lang.lower() == language.lower():
        language = num
    if type(language2) is str and lang.lower() == language2.lower():
        language2 = num


if type(language2) is str and language2.lower() == "all":
    language2 = 0

file = open(word + ".txt", 'w', encoding='UTF-8')

if language2 == 0:
    for i in LANGUAGES.keys():
        if i == language:
            continue
        translate(language, i, word, file)
else:
    translate(language, language2, word, file)
file.close()

file = open(word + ".txt", 'r', encoding='UTF-8')
print(file.read())
