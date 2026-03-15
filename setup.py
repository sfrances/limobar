from setuptools import setup

APP = ['LimoBar.py']

OPTIONS = {
    'argv_emulation': False,
    'packages': ['pyotp'],
    'includes': ['objc', 'Foundation', 'AppKit'],
    'plist': {
        'LSUIElement': True  # prevents Dock icon (menu bar apps)
    }
}

setup(
    app=APP,
    name="LimoBar",
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)