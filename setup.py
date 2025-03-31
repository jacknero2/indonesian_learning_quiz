from setuptools import setup

APP = ['chatgpt_quiz_app.py']
OPTIONS = {
    'argv_emulation': True,
    'excludes': [
        'PyInstaller.hooks.hook-PySide6.QtBluetooth',
        'PyInstaller.hooks.hook-PyQt6.QtNetworkAuth',
        'PyInstaller.hooks.hook-PyQt5.QtNetwork',
        'packaging',  # Exclude packaging to avoid duplicate copies
    ],
    'packages': ['pandas', 'pygame', 'PIL'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['pandas', 'pygame', 'Pillow']
)
