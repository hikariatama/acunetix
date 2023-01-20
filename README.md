[![DeepSource](https://deepsource.io/gh/hikariatama/acunetix.svg/?label=active+issues&show_trend=true&token=IPVI_QX-cSuQSVeVl8cb5PLt)](https://deepsource.io/gh/hikariatama/acunetix/?ref=repository-badge)  

[![DeepSource](https://deepsource.io/gh/hikariatama/acunetix.svg/?label=resolved+issues&show_trend=true&token=IPVI_QX-cSuQSVeVl8cb5PLt)](https://deepsource.io/gh/hikariatama/acunetix/?ref=repository-badge)  

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/hikariatama/acunetix)
![GitHub repo size](https://img.shields.io/github/repo-size/hikariatama/acunetix)
![License](https://img.shields.io/github/license/hikariatama/acunetix)
![Forks](https://img.shields.io/github/forks/hikariatama/acunetix?style=flat)
![Stars](https://img.shields.io/github/stars/hikariatama/acunetix?style=flat)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# SDK for Acunetix Web Vulnerability Scanner

## Installation

```bash
pip install acunetix
```

## Usage

```python
import asyncio
from acunetix import AcunetixAPI

async def main():
    api = AcunetixAPI("TOKEN", "localhost:3443")
    await api.connect()
    result = await api.default_scan(InputTarget("https://hikariatama.ru"))
    print(result)

asyncio.run(main())
```

## License

[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)

## Docs

Documentation is not ready yet, but you can read the source code.

