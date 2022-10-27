# Onliner Parser

## Features
- Parsing product categories
- Importing retrieved information into csv or xlsx

------------

## Installation and setup
1. Clone the repository
`git clone https://github.com/devShev/onliner-parser.git`

2. Select the desired category in your browser

    ![](https://i.ibb.co/1qq9wtS/image.png)

3. Copy the URL from your browser's address bar

    ![](https://i.ibb.co/09Q0xmh/image.png)

4. Go to the app.py file and paste your URL, you get the following code
```python
url = 'your url'

parser = CatalogParser(url)
parser.parse()

saver = SaveManager(Product, parser.get_data())
saver.save()
```

***Setup complete***

------------

## Parser methods:
### parse()
- Gather information from directory

### get_data()
- Return received information in the form of a list of objects

### Save manager methods:

### save(filename: str, save_format: str)
Saves the obtained information into a file
- filename - the name of the file to be created (optional parameter, by default - 'products')
- save_format - the file format (csv / xlsx) (optional parameter, by default - csv)

### set_directory_name(name: str)
Sets the name of directory where files are saved (default - 'data/')
- name - the directory name (required parameter)