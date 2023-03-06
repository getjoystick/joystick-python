#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


setup(
    name="joystick-python",
    version="0.1.0-alpha.1",
    license="MIT",
    description=(
        "Joystick is a modern remote configuration and dynamic content service designed "
        "specifically for operating apps and games. Upgrade to more agility and evolve "
        "your product faster. Change or hot-update your content and configurations "
        "instantly at scale without code. Segment, ab test, feature flag, schedule events "
        "and more. Joystick is a breeze to use yet powerful."
    ),
    long_description="{}\n{}".format(read("README.md"), read("CHANGELOG.md")),
    long_description_content_type="text/markdown",
    author="Joystick",
    author_email="letsgo@getjoystick.com",
    url="https://github.com/getjoystick/getjoystick/joystick-python",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    project_urls={
        "Changelog": "https://github.com/getjoystick/joystick-python/blob/main/CHANGELOG.md",
        "Issue Tracker": "https://github.com/getjoystick/joystick-python/issues",
    },
    keywords=[
        "Remote configuration",
        "feature flagging",
        "dynamic content",
        "remote configs",
        "live-ops",
        "game ops",
        "ab testing",
        "segmentation",
        "dynamic json",
        "update json",
        "remote json",
    ],
    python_requires=">=3.6",
    install_requires=["httpx[http2]>=0.23.3,<1.0", "pylru>=1.2.1,<2.0.0"],
    extras_require={"dev": ["nox", "wheel"]},
)
