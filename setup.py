"""!
@author atomicfruitcake

@date 2020
"""

import pathlib
from setuptools import setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="gnutty",
    version="1.0.0",
    description="Pure Python REST HTTP Server",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/reader",
    author="atomicfruitcake",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["gnutty"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
