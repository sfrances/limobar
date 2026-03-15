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
    version="0.2",
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    packages=["limobar"],
    include_package_data=True,  # Ensure package data is included
    package_data={
        "": ["tokens.json"],  # Include tokens.json in the package
    },
)