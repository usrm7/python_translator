import inquirer
import json
import requests
from ast import literal_eval

language_list = {
    "English": "en",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Chinese": "zh",
    "Japanese": "ja",
    "Russian": "ru",
}

choices = [
    "English",
    "French",
    "German",
    "Spanish",
    "Italian",
    "Chinese",
    "Japanese",
    "Russian",
]


def select_source_language():
    questions = [
        inquirer.List(
            "source_language",
            message="Translate FROM what language? ",
            choices=choices,
        ),
    ]
    answers = inquirer.prompt(questions)
    source_language = language_list.get(answers["source_language"])
    return source_language


def select_target_language():
    questions = [
        inquirer.List(
            "target_language",
            message="Translate TO what language? ",
            choices=choices,
        ),
    ]
    answers = inquirer.prompt(questions)
    target_language = language_list.get(answers["target_language"])
    return target_language


def getJson(my_bytes_value):
    data = literal_eval(my_bytes_value.decode("utf-8"))
    s = json.dumps(data)

    # need to convert it into a dictionary so we can access the elements
    s_dict = json.loads(s)

    # for now, just show the translation
    print("Translation: " + s_dict["sentences"][0]["trans"])


def make_translation_request():
    sl_value = select_source_language()
    tl_value = select_target_language()
    if sl_value == tl_value:
        print("Source and target language cannot be the same. Please try again.")
        return
    else:
        q_value = input("Please type the text to translate. \nOriginal: ")

    # example curl command for Google Translate:
    # curl --location --request POST 'https://translate.google.com/translate_a/single?client=at&dt=t&dt=ld&dt=qca&dt=rm&dt=bd&dj=1&hl=%25s&ie=UTF-8&oe=UTF-8&inputm=2&otf=2&iid=1dd3b944-fa62-4b55-b330-74909a99969e&' \
    # --header 'Content-Type: application/x-www-form-urlencoded' \
    # --header 'User-Agent: AndroidTranslate/5.3.0.RC02.130475354-53000263 5.1 phone TRANSLATE_OPM5_TEST_1' \
    # --data-urlencode 'sl=de' \
    # --data-urlencode 'tl=en' \
    # --data-urlencode 'q=Hallo'

    # curl broken up into a Python request library format.  This is preferred to
    # running some type of curl-like command inside the python file - https://stackoverflow.com/a/31764155

    # getting the curl command broken up can be done mostly using this tool(https://github.com/NickCarneiro/curlconverter),
    # online version (https://curl.trillworks.com/), with some changes mostly to the params section

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "AndroidTranslate/5.3.0.RC02.130475354-53000263 5.1 phone TRANSLATE_OPM5_TEST_1",
    }

    query_tuple = (
        ("sl", {sl_value}),
        ("tl", {tl_value}),
        ("q", {q_value}),
    )

    params = (
                 ("client", "at"),
                 ("dt", ["t", "ld", "qca", "rm", "bd"]),
                 ("dj", "1"),
                 ("hl", "%s"),
                 ("ie", "UTF-8"),
                 ("oe", "UTF-8"),
                 ("inputm", "2"),
                 ("otf", "2"),
                 ("iid", "1dd3b944-fa62-4b55-b330-74909a99969e"),
             ) + query_tuple

    response = requests.post(
        "https://translate.google.com/translate_a/single",
        headers=headers,
        params=params,
    )
    # will send bytes
    getJson(response.content)


make_translation_request()
