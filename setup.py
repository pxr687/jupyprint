from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="jupyprint",
    version="0.1.2",
    author="Peter Rush",
    description="A simple python package to print markdown and LaTeX equations from code cells in Jupyter notebooks.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
    "numpy",
    "pandas",
    "ipython"
    ],
)
