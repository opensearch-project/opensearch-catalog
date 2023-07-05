from setuptools import find_packages, setup

setup(
    name="osints",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "beartype",
        "click",
    ],
    python_requires=">3.10.0",
    entry_points={"console_scripts": ["osints = src.main:cli"]},
)
