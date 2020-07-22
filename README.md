# Piktok

Piktok is a Python library for retrieving public data from TikTok.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install piktok.

```bash
pip install piktok
```

## Usage

```python
from piktok import App


proxy = ... # url str or None

app = App(proxy=proxy)

# every functions are async - make sure to implement accordingly
await app.discover.user()
await app.discover.music()
await app.suggested.fetch()
await app.info.user_by_name('fpgezekatz')
await app.tiktoks.from_user_id(6834564640216974341, total=200)
await app.suggested.crawl(7, 3, user_id=143273922984189952, user_count=30)
```

## Documentation
https://anh-chu.github.io/piktok/

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)