from onliner_parser import Product, CatalogParser, SaveManager


parser = CatalogParser('https://catalog.onliner.by/mobile')
parser.deep_parse()

manager = SaveManager(Product, parser.get_data())

manager.save_csv()
