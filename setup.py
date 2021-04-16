from setuptools import setup
import setuptools


# read description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="exemplo_pytest",
    version="1.9",
    author="MATHEUS",
    author_email="matheus.santos@enacom.com.br",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    description="Exemplo Pytest"
)

