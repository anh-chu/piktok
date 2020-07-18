# Piktok

Piktok is a Python library for retrieving public data from TikTok.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install piktok.

```bash
pip install git+git://github.com/anh-chu/piktok.git#egg=piktok
```

## Usage

```python
from piktok import App


app = App(proxy="")

app.tiktoks.from_user(user_id=...) # returns tiktoks by the user
app.suggested.fetch() # returns suggested musics, challenges, and users
app.discover.music() # retuns music from the discover page
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)