from setuptools import find_packages, setup

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
    version='0.2.2',
    description='Парсер для каталога Onliner.by',
    packages=find_packages(),
    install_requires=requirements,
    author_email='aalshe38@gmail.com',
    zip_safe=False,
)
