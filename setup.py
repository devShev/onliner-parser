from setuptools import setup

requirements = [
    "pydantic==1.10.2",
    "requests==2.28.1",
    "progress==1.6",
    "pandas==1.5.0",
    "openpyxl==3.0.10",
    "beautifulsoup4==4.11.1",
]

setup(
    name='onliner_parser',
    version='0.2.1',
    description='Парсер для каталога Onliner.by',
    packages=['onliner_parser'],
    install_requires=requirements,
    author_email='aalshe38@gmail.com',
    zip_safe=False,
)
