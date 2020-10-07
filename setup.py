import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="esrel",
    version="0.0.1",
    author="Evgeny A. Stepanov",
    author_email="stepanov.evgeny.a@gmail.com",
    description="NLP Utilities for Language Understanding Lab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/esrel/LUS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: LGPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
