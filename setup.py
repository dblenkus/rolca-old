from setuptools import setup, find_packages

setup(
    name="Rolca",
    version="0.1",
    url='https://github.com/dblenkus/rolca',
    author="Domen Blenkus",
    author_email="domen@blenkus.com",

    description="Webapp for organizing fiap and other salons.",
    long_description=open('README.md', 'r').read(),
    license="AGPL3",

    packages=find_packages(),
)
