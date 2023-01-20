from setuptools import setup, find_packages

setup(
    name="acunetix",
    version="0.0.3",
    packages=find_packages(),
    long_description="Acunetix Web Vulnerability Scanner API wrapper",
    keywords="acunetix vulnerability scanner pentest security infosec",
    python_requires=">=3.6",
    author="Daniil Gazizullin",
    author_email="me@hikariatama.ru",
    url="https://github.com/hikariatama/acunetix",
    download_url="https://github.com/hikariatama/acunetix/releases",
    install_requires=["aiofiles", "aiohttp"],
)
