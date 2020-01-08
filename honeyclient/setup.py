import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "tr069", "__init__.py")) as f:
    __version__ = f.read().split("__version__ = '", 1)[1].split("'", 1)[0]

setup(
    name="tr069",
    version=__version__,
    description="A TR-069 Library in Python",
    url="https://github.com/mhils/tr069",
    author="Maximilian Hils",
    author_email="tr069@maximilianhils.com",
    packages=find_packages(include=["tr069", "tr069.*"]),
    include_package_data=True,
    install_requires=[
        "click~=6.7",
        "requests~=2.13.0",
        "beautifulsoup4~=4.5.3",
    ],
    extras_require={
        'dev': [
            "hypothesis~=3.6.1",
        ],
        'pretty': [
            "mitmproxy~=2.0.0",
            "pygments~=2.2.0",
        ],
    },
    entry_points={
        'console_scripts': [
            "tr069-client = tr069.__main__:cli",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
)
