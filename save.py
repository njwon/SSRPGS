from cryptors import encrypt, decrypt
from re import finditer
import json

class Save:
    def __init__(self):
        self.save_file_name = ""
        
        self.save_json = {}
        self.save_slots = []
        self.save_slot = ""
        
    def __getitem__(self, key):
        return self.save_json[self.save_slot][key]
    
    def __setitem__(self, key, value):
        self.save_json[self.save_slot][key] = value

    def is_loaded(self):
        return self.save_slot != ""
    
    def jsonize(self, text):
        text = text.replace('\n\t', '\n')
        text = text.replace('\\[', '\\\\［')
        text = text.replace('\\]', '\\\\］')

        # Escape array values (colons)
        shift = 0
        for m in finditer(r"\".*?\"|\[([^{]+?,)*?[^{]*?\]", text):
            if m.group(0)[0] != "[":
                continue
            
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

            if text[start] == '"':
                continue

            if value.count(":") == 0:
                text = f'{text[:start]}"{value}"{text[end:]}'
                shift += 2

            elif value.count(":") >= 1:
                key, value = value.split(":", 1)

                # Replace boolean values by JSON format
                if value == "True":
                    value = "true"
                
                if value == "False":
                    value = "false"

                if not value or value[0] == '"' or value.replace("-", "").replace(".", "", 1).isdigit() or value in ("false", "true"):
                    text = f'{text[:start]}"{key}":{value}{text[end:]}'
                    shift += 2
                else:
                    text = f'{text[:start]}"{key}":"{value}"{text[end:]}'
                    shift += 4
        
        text = text.replace('\\\\［', '\\\\[')
        text = text.replace('\\\\］', '\\\\]')

        return text
    
    def open(self, save_file_name):
        jsonized = self.jsonize(open(save_file_name, "r", encoding="utf-8").read())
        
        self.save_file_name = save_file_name
        self.save_json = json.loads(jsonized)
        self.save_slots = []

        # Decrypt all saves in file
        for field in self.save_json:
            if field.startswith("save_file_") and field != "save_file_last_id":
                self.save_slots.append(field)

                # Decrypt only crypted blocks
                if self.save_json[field]["encrypted"] != True:
                    continue

                progress_data = decrypt(self.save_json[field]["progress_data"])
                progress_json = self.jsonize(progress_data)
                
                print("SLIM_JSON:", progress_data)
                print("JSONIZED_TEXT:", progress_json)

                self.save_json[field]["progress_data"] = json.loads(progress_json)

        # Change encrypted to False for all saves
        for save_slot in self.save_slots:
            self.save_json[save_slot]["encrypted"] = False

        # Select last save as actual
        self.save_slot = f"save_file_{self.save_json["save_file_last_id"]}"

    def sjsonize(self, save_json):
        text = ""

        # Convert boolean values by SJSON format
        def bool_to_sjson(dictionary):
            for key in dictionary:
                if isinstance(dictionary[key], bool):
                    dictionary[key] = str(dictionary[key])
                if isinstance(dictionary[key], dict):
                    bool_to_sjson(dictionary[key])
        
        bool_to_sjson(save_json)
        text = json.dumps(save_json, separators=(",", ":"), ensure_ascii=False)

        # Remove quotes where it's possible
        shift = 0
        for match in finditer(r"\".*?\"", text):
            start = match.start() + shift
            end = match.end() + shift

            value = text[start:end]
            
            if value.count('"') > 2 or value == '""' or value[1] == " " or value.count(",") or (value.count("[") + value.count("]")):
                continue

            text = f'{text[:start]}{value[1:-1]}{text[end:]}'
            shift -= 2

        text = text.replace('\\\\[', '\\[')
        text = text.replace('\\\\]', '\\]')

        return text

    def save(self, file_name=None):
        if file_name is None:
            file_name = self.save_file_name

        sjsonized = self.sjsonize(self.save_json)
        with open(file_name, "w", encoding="utf-8") as j:
            j.write(sjsonized)

    def open_from_json(self, save_file_name):
        self.save_file_name = save_file_name
        
        self.save_json = json.load(open(save_file_name))
        self.save_slots = []
        for field in self.save_json:
            if field.startswith("save_file_") and field != "save_file_last_id":
                self.save_slots.append(field)
        self.save_slot = f"save_file_{self.save_json["save_file_last_id"]}"

    def save_as_json(self, file_name):
        with open(file_name, "w", encoding="utf-8") as j:
            j.write(json.dumps(self.save_json, indent=4, ensure_ascii=False))

# Load from json and write
# save = Save()
# save.open("primary_save.txt")
# save.save_as_json("del.json")
# save.save("del.txt")

# save = Save()
# save.save_json = json.load(open("formatted.json"))
# save.save("primary_save.txt")

# Get all unique tags from inventory items
# unique = {}
# def unroll(item, layer=0):
#     if layer not in unique:
#         unique[layer] = set()

#     for key in item:
#         unique[layer].add(key)
        
#         if isinstance(item[key], dict):
#             unroll(item[key], layer+1)

# for item in save.save_json["save_file_40"]["progress_data"]["inventory_data"]["itms"]:
#     unroll(item)

# from pprint import pprint
# pprint(unique)
