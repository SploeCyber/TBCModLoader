import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("src/bcgm_mod_manager/files/version.txt", "r", encoding="utf-8") as fh:
    version = fh.read()

setuptools.setup(
    name="bcgm_mod_manager",
    version=version,
    author="fieryhenry",
    description="A battle cats game modding tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fieryhenry/bcgm_mod_manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "alive_progress",
        "beautifulsoup4",
		"colored",
        "Pillow"
        "pycryptodomex",
		"PyYAML",
        "requests",
    ],
    include_package_data=True,
    extras_require={
        "testing": [
            "pytest",
            "pytest-cov",
        ],
    },
    package_data={"bcgm_mod_manager": ["py.typed"]},
    flake8={"max-line-length": 160},
)
