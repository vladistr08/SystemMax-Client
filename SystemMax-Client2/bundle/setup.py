from setuptools import setup

APP = ['/Users/istra/Programare/SystemMax/SystemMax-Client/SystemMax-Client2/main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PySide6'],
    'resources': ['/opt/homebrew/Cellar/libffi/3.4.6/lib/libffi.8.dylib'],
    'plist': {
        'CFBundleName': 'SystemMax',
        'CFBundleDisplayName': 'SystemMax',
        'CFBundleVersion': '0.1',
        'CFBundleShortVersionString': '0.1',
        'CFBundleIdentifier': "com.example.systemmax",
        'CFBundleIconFile': '/Users/istra/Programare/SystemMax/SystemMax-Client/SystemMax-Client2/res/logo-removebg.png',
    },
}

setup(
    app=APP,
    name='SystemMax',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)