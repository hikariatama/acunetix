from setuptools import setup, find_packages
import os
import pathlib

setup(
    name="acunetix",
    version="0.0.2",
    packages=find_packages(),
    long_description=pathlib.Path(
        os.path.join(os.path.dirname(__file__), "README.md")
    ).read_text(),
)
