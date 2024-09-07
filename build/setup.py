# MacOS installer
# Usage: make all

from setuptools import setup

APP = ["../src/editor.py"]

APP_NAME = "Stone Story RPG Save editor"

DATA_FILES = [
    "../src/translations",
    "../src/fonts",
    "../src/images",
    "../src/settings.toml",
    ("save", [
        "../src/save/save_file.py",
        "../src/save/get_file.py"
    ]),
]

OPTIONS = {
    'iconfile': '../src/images/icon.icns',
    "packages": [
        "dearpygui",
        "natsort",
        "pprp",
        "pyperclip"
    ],
    "includes": [
        "tkinter.filedialog",
        "os.remove",
        "os.path",
        "os.name",
        "sys.argv",
        "getpass.getuser"
    ],
    "plist": {
        "CFBundleName": APP_NAME,
        "CFBundleDisplayName": APP_NAME,
        "CFBundleGetInfoString": "Mouse can walk",
        "CFBundleIdentifier": "com.catalyst.mousewalk",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "NSHumanReadableCopyright": u"Copyright © 2024, Catalyst",
        "LSUIElement": True
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={
        "py2app": OPTIONS
    },
    setup_requires=["py2app"]
)
