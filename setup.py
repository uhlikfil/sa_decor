import os

import setuptools


def get_version() -> str:
    return os.getenv("GITHUB_REF_NAME")[1:]


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="sa_decor",
    version=get_version(),
    author="Filip Uhlík",
    author_email="filipfilauhlik@gmail.com",
    description="SQLAlchemy decorators for an optional connection/session dependency injection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uhlikfil/sa_decor",
    project_urls={
        "Bug Tracker": "https://github.com/uhlikfil/sa_decor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "./"},
    packages=("sa_decor",),
    python_requires=">=3.7",
)
