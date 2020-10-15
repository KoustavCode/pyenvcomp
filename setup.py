import pathlib
from setuptools import setup
from pyenvcomp import __version__

with open('README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

# This call to setup() does all the work
setup(
    name="pyenvcomp",
    version=__version__,
    description="Detailed display of the difference between two given python virtual environments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KoustavCode/pyenvcomp.git",
    author="Koustav Chanda",
    author_email="koustavtocode@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["pyenvcomp"],
    include_package_data=True,
    install_requires=['tableformatter'],
    entry_points={
        "console_scripts": [
            "compare=pyenvcomp.main:main",
        ]
    },
)