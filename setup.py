from setuptools import setup, find_packages

setup(
    name="janitor",
    version="1.0.0",
    author="Greg Anders",
    author_email="greg@gpanders.com",
    description="Clean up filesystem paths",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gpanders/janitor",
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={
        "console_scripts": [
            "janitor = janitor.console:run",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
