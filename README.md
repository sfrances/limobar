This app just craeting a simple menu in the MacOS menu bar, and show some custom content when click the menu items. For now it manages personal TOPTs only but it can be easily expanded.

## Dependencies

Just need `python3`, `pyobjc`, `pyotp`  and `py2app` packages. I recommend using a simple virtual environment to install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the app

Prepare your OTP tokens in the `tokens.json` file, in the form of a simple dictionary:

```json
{
    "GitHub" : "XXXXXXXXXXXXXX",
    "GitLab"   : "YYYYYYYYYYYYYY"
}
```
No format check is enforced for now.

Be sure the app is an executable file, then just run it:

```bash
chmod +x LimoBar.py
```
and then run it:

```bash
./LimoBar.py
```

## Make it a real app

To make it a real app, you can use `py2app` to create a standalone application bundle. Just run the following command (inside the virtual environment if you are using one):

```bash
python setup.py py2app
```

