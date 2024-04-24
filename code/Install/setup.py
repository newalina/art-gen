from setuptools import setup, find_packages

setup(
    name="art-gen",
    version="1.0",
    author="Alec Pratt",
    packages=find_packages(where=".."),
    package_dir={'': '..'},
)