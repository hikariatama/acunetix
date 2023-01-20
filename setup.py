from setuptools import setup, find_packages
import os
import pathlib
import version

setup(
    name="acunetix",
    version=version.__version__,
    packages=find_packages(),
    long_description=pathlib.Path(
        os.path.join(os.path.dirname(__file__), "README.md")
    ).read_text(),
)
