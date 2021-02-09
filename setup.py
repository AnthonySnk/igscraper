#!/usr/bin/env python3.8

from setuptools import setup, find_packages

setup(
    name="igscraper",
    version="20.02.8",
    description="Instagram scraper",
    author="jxlil",
    url="https://github.com/jxlil/igscraper",
    packages=find_packages(),
    install_requires=[
        "instagram_private_api",
        "yaspin",
        "PyYAML",
    ],
    license="MIT",
    classifiers=["Programming Language :: Python :: 3"],
)
