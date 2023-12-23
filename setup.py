from setuptools import setup, find_packages

setup(
    name="jupyprint",
    version="0.1.0",
    author="Peter Rush",
    description="A simple python package to print markdown/LaTeX in Jupyter notebooks.",
    long_description="Please see the README here: https://github.com/pxr687/jupyprint",
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
