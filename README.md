# Password_generator
Easily generate new password that cannot be easily guessed.
![pass1](https://github.com/SonOfGod04/Password_generator/blob/main/Screenshot%20(92).png)

A small desktop app that generates strong random passwords. It is built with Tkinter and has no third-party dependencies.

The generation logic lives in its own module (`password_core.py`), so you can use it without the GUI.

## Features

- Cryptographically secure randomness via Python's `secrets` module
- Length from 8 to 128 characters (default 16)
- Choose lowercase, uppercase, digits and symbols
- Option to avoid look-alike characters (`I`, `l`, `1`, `O`, `0`, `o`)
- At least one character from every selected type is guaranteed
- Strength label with an approximate entropy estimate
- Password shown in a read-only field, never in a pop-up
- One-click copy, with the clipboard cleared automatically after 30 seconds (only if you haven't copied something else since)
- Inline error messages instead of crashes on invalid input

## Requirements

- Python 3.10 or newer
- Tkinter (bundled with the official Python installers for Windows and macOS)

On Debian/Ubuntu, Tkinter is a separate package:

```bash
sudo apt install python3-tk
```

## Installation

```bash
git clone https://github.com/SonOfGod04/password-generator.git
cd password-generator
```

No `pip install` step is needed.

## Usage

### Desktop app

```bash
python password_generator.py
```

Adjust the length and options, and a new password is generated automatically. Press **Enter** or click **Generate** for another one, and **Copy** to put it on the clipboard.

### As a library

```python
from password_core import generate_password, estimate_entropy_bits

pw = generate_password(20, symbols=False)
bits = estimate_entropy_bits(20, symbols=False)
```

Options (all `bool`, all default to `True` except `exclude_ambiguous`): `lower`, `upper`, `digits`, `symbols`, `exclude_ambiguous`.

`generate_password` raises `ValueError` if the length is out of range or no character type is selected.


![pass1](https://github.com/SonOfGod04/Password_generator/blob/main/Screenshot%20(95).png)
## Running the tests

```bash
python -m unittest
```

or, if you use pytest:

```bash
pytest
```

The tests cover the core module only, so they run on machines without Tkinter (for example CI servers).

## Project structure

```
password_core.py             Password generation and strength estimate (no GUI)
password_generator.py        Tkinter interface
test_password_generator.py   Unit tests for the core module
```

## Security notes

- Passwords are generated locally and are never stored, logged or sent anywhere.
- The strength figure is an estimate (`length × log2(alphabet size)`). The guarantee of one character per selected type slightly lowers real entropy, so treat the number as a guide, not a measurement.
- The clipboard clear only works while the app is open. Closing the window before the timer ends leaves the password on the clipboard, and clipboard managers or history tools may keep their own copy.
- For important accounts, store passwords in a reputable password manager rather than memorising or reusing them.

## Contributing

Issues and pull requests are welcome. Please run the tests before opening a PR.
![pass1](https://github.com/SonOfGod04/Password_generator/blob/main/Screenshot%20(96).png)

