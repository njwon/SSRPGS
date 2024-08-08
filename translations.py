import locale
import tomllib
import json

languages = {
    "ru": "Русский",
    "en": "English"
}

with open("settings.toml", "rb") as f:
    settings = tomllib.load(f)
    language = settings["language"]
    is_auto = language == "auto"

    # Try to set system language
    if is_auto:
        system_language, _ = locale.getlocale()
        print(f"System language is {system_language}")
        
        if system_language:
            language = system_language[:2]

    if language not in languages:
        language = "en"

    i18n = json.load(open(f"translations/{language}.json"))

def configure_language(_, language):
    for code in languages:
        if languages[code] != language:
            continue

        with open("settings.toml", "w") as config:
            config.write(f'language = "{code}"\n')
            print(f"Default language is set to {code}")
            return
