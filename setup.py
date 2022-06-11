import setuptools
from setuptools.command.egg_info import egg_info


class egg_info_ex(egg_info):
    """Includes license file into `.egg-info` folder."""

    def run(self):
        # don't duplicate license into `.egg-info` when building a distribution
        if not self.distribution.have_run.get("install", True):
            # `install` command is in progress, copy license
            self.mkpath(self.egg_info)
            self.copy_file("LICENSE.txt", self.egg_info)

        egg_info.run(self)


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="sa_decor",
    version="1.0.0",
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
