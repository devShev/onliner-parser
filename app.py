from onliner_parser import CatalogParser
from onliner_parser.managers import SaveManager

parser = CatalogParser('https://catalog.onliner.by/selfiestick')
parser.deep_parse()

print(parser.get_data()[0])

saver = SaveManager(parser.get_data())
saver.save()
