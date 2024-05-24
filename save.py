from cryptors import encrypt, decrypt
from re import finditer
import json

from cryptors import decrypt

class Save:
    def __init__(self, file_name):
        self.file_name = file_name
        self.save_file = open(file_name, "r", encoding="utf-8").read()
        self.save_json = {}

        self.save_slots = []
        
        self.open()

    def jsonize(self, text):
        text = text.replace('\n\t', '\n')

        # Escape array values (colons)
        shift = 0
        for m in finditer(r"\[([^{]+?,)*?[^{]*?\]", text):
            array = m.group(0).replace("\n", '')
            start_len = len(m.group(0))
            inner_shift = 0
            for match in finditer(r"\".*?\"|[^,\[\]]+", array):
                start = match.start() + inner_shift
                end = match.end() + inner_shift

                value = array[start:end]

                if value[0] != '"':
                    array = f'{array[:start]}"{value}"{array[end:]}'
                    inner_shift += 2
            
            start = m.start() + shift
            end = m.end() + shift
            text = f'{text[:start]}{array}{text[end:]}'
            shift += -start_len + len(array)
            
        # Add quotes to all values
        shift = 0
        for match in finditer(r"\".*?\"|[^{}\[\],\n\"]+", text):
            start = match.start() + shift
            end = match.end() + shift

            value = text[start:end]
            if value[0] == '"':
                continue

            if value.count(":") == 0:
                text = f'{text[:start]}"{value}"{text[end:]}'
                shift += 2

            elif value.count(":") >= 1:
                key, value = value.split(":", 1)

                if not value or value[0] == '"' or value.replace("-", "").replace(".", "", 1).isdigit():
                    text = f'{text[:start]}"{key}":{value}{text[end:]}'
                    shift += 2
                else:
                    text = f'{text[:start]}"{key}":"{value}"{text[end:]}'
                    shift += 4
        
        return text

    def open(self):
        jsonized = self.jsonize(self.save_file)
        self.save_json = json.loads(jsonized)
        self.save_slots = []

        # Decrypt all saves in file
        for value in self.save_json:
            if value.startswith("save_file_") and value != "save_file_last_id":
                self.save_slots.append(value)

                progress_data = decrypt(self.save_json[value]["progress_data"])
                progress_json = self.jsonize(progress_data)
                self.save_json[value]["progress_data"] = json.loads(progress_json)

        # Change encrypted to False for all saves
        for save_slot in self.save_slots:
            self.save_json[save_slot]["encrypted"] = "False"

    def sjsonize(self, save_json):
        text = ""
        text = json.dumps(save_json, separators=(",", ":"), ensure_ascii=False)

        # Remove quotes where it's possible
        shift = 0
        for match in finditer(r"\".*?\"", text):
            start = match.start() + shift
            end = match.end() + shift

            value = text[start:end]

            if value.count('"') > 2 or value == '""' or value[1] == " " or value.count(","):
                continue

            if value == '"true"':
                value = '"True"'

            if value == '"false"':
                value = '"False"'

            text = f'{text[:start]}{value[1:-1]}{text[end:]}'
            shift -= 2

        return text

    def save(self, file_name):
        sjsonized = self.sjsonize(self.save_json)
        with open(file_name, "w", encoding="utf-8") as j:
            j.write(sjsonized)

# Usage
# save = Save("save.txt")
# save.save_json["save_file_42"]["player_name"] = "LOCALHOST"
# save.save_json["save_file_42"]["progress_data"]["hero_settings"]["playerName"] = "LOCALHOST"
# save.save("primary_save.txt")
