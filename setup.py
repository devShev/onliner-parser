from setuptools import setup, find_packages

requirements = [
    "pydantic",
    "requests",
    "progress",
    "pandas",
    "openpyxl",
    "beautifulsoup4",
]

setup(
    name='onliner_parser',
    version='0.2.1.1',
    description='Парсер для каталога Onliner.by',
    packages=find_packages(),
    install_requires=requirements,
    author_email='aalshe38@gmail.com',
    zip_safe=False,
)
