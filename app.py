from onliner_parser import CatalogParser
from onliner_parser.managers import SaveManager

from progress.bar import IncrementalBar

parser = CatalogParser('https://catalog.onliner.by/selfiestick')
parser.parse()

bar = IncrementalBar('APP', max=parser.get_items_count())  # Код, который отправляет сообщение с прогрессом

while parser.parse_next():
    bar.next()  # Код, который будет менять сообщение с прогрессом
bar.next()


saver = SaveManager(parser.get_data())
saver.save()
