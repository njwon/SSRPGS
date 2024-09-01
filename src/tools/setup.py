import locale
import tomllib
import json

from os import name

WIDTH = 600
HEIGHT = 394

OFFSET = 0
SCALE = 1

REMAP_START = 0x10ec77
REMAP_END = 0x10ffff

IS_NT = name == "nt"  # Windows

# Load settings
with open("settings.toml", "rb") as f:
    settings = tomllib.load(f)

# Translations
languages = {
    "ru": "Русский",
    "en": "English"
}

class TranslationDict:
    def __init__(self, value):
        self.value = value

    def __getitem__(self, key):
        if key in self.value:
            return TranslationDict(self.value[key])
        return TranslationDict(key)

    def __setitem__(self, name, new_value):
        self.value[name] = new_value

    def __add__(self, other):
        return self.value + other

    def __repr__(self):
        return str(self.value)

def get_language():
    language = settings["language"]
    is_auto = language == "auto"

    # Try to set system language
    if is_auto:
        system_language, _ = locale.getdefaultlocale()
        print(f"System language is {system_language}")

        if system_language:
            language = system_language[:2]

    if language not in languages:
        language = "en"

    return language

def configure_language(_, language):
    for code in languages:
        if languages[code] != language:
            continue

        update_settings(language=code)
        print(f"Default language is set to {code}")

def configure_scale(_, scale):
    print(f"Upscale is set to {scale}")
    update_settings(upscale=str(scale).lower())

def update_settings(language="auto", upscale="false"):
    with open("settings.toml", "w", encoding="utf-8") as config:
        config.write(f'language = "{language}"\n')
        config.write(f'upscale = {upscale}\n')

# Load translation dict
i18n = TranslationDict(
    json.load(
        open(
            f"translations/{get_language()}.json",
            encoding="utf-8"
        )
    )
)

# Check things for nt
if IS_NT:
    i18n["title"] = "Stone Story RPG save editor"  # DPG don't support latin title on NT
    OFFSET = 38  # Windows title bar

    if settings["upscale"]:
        OFFSET = -47  # Smaler gaps between widgets
        SCALE = 2

        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
