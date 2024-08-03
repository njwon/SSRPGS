import tomllib
import json

available_languages = [
    "Русский",
    "English"
]

with open("settings.toml", "rb") as f:
    settings = tomllib.load(f)
    language = settings["language"]
    
    if language == "auto":
        pass  # TODO: You know...
        
        i18n = None
        i18n["language-name"] = i18n["language-auto"]

    else:
        i18n = json.load(open(f"translations/{language}.json"))

# TODO: Remove "epic" from names