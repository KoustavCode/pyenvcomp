import pathlib
from setuptools import setup
from pyenvcomp import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyenvcomp",
    version=__version__,
    description="Detailed display of the difference between two given python virtual environments.",
    long_description=README,
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
    install_requires=[],
    entry_points={
        "console_scripts": [
            "compare=pyenvcomp.main:main",
        ]
    },
)