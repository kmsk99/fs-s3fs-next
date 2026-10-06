#!/usr/bin/env python

from setuptools import setup, find_packages

with open("fs_s3fs/_version.py") as f:
    exec(f.read())

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Programming Language :: Python :: 3.15",
    "Topic :: System :: Filesystems",
]

with open("README.rst", "rt") as f:
    DESCRIPTION = f.read()

REQUIREMENTS = [
    "boto3~=1.9",
    "fs-next>=0.1.1,<0.2",
    "six~=1.10",
]

setup(
    name="fs-s3fs-next",
    author="Will McGugan",
    author_email="willmcgugan@gmail.com",
    classifiers=CLASSIFIERS,
    description="Amazon S3 filesystem for FS Next, an independent fs-s3fs maintenance fork",
    install_requires=REQUIREMENTS,
    license_expression="MIT",
    long_description=DESCRIPTION,
    packages=find_packages(),
    keywords=["pyfilesystem", "Amazon", "s3"],
    platforms=["any"],
    python_requires=">=3.10",
    maintainer="Mason Kim",
    long_description_content_type="text/x-rst",
    url="https://github.com/kmsk99/fs-s3fs-next",
    version=__version__,
    entry_points={"fs.opener": ["s3 = fs_s3fs.opener:S3FSOpener"]},
)
