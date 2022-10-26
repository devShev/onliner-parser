from onliner_parser import CatalogParser
from onliner_parser.managers import SaveManager

parser = CatalogParser('https://catalog.onliner.by/selfiestick')

parser.async_deep_parse()

saver = SaveManager(parser.get_data(), parser.SETTINGS)
saver.save()
