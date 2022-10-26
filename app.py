from onliner_parser import CatalogParser
from onliner_parser.managers import SaveManager

parser = CatalogParser('https://catalog.onliner.by/selfiestick')

parser.SETTINGS.parse_spec = False

parser.deep_parse()

saver = SaveManager(parser.get_data(), parser.SETTINGS)
saver.save()
