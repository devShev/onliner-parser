import argparse
import os


class InputManager:
    @staticmethod
    def get_args() -> dict:
        if not os.environ.get("IS_DOCKER", False):
            arg_parser = argparse.ArgumentParser(description='Parser Catalog Onliner')

            arg_parser.add_argument(
                '-u',
                dest='url',
                type=str,
                help='URL category',
                required=True,
            )

            arg_parser.add_argument(
                '-fn',
                dest='filename',
                type=str,
                help='The name of the file to which the data will be saved (standard - products)',
                default='products',
                required=False,
            )

            arg_parser.add_argument(
                '-sf',
                dest='save_format',
                type=str,
                help='Format for saving data (csv/xlsx) (standard - csv)',
                default='csv',
                required=False,
            )

            args = arg_parser.parse_args()

            url = args.url
            filename = args.filename
            save_format = args.save_format
        else:
            url = os.environ.get("URL")
            filename = os.environ.get("FILENAME", "products")
            save_format = os.environ.get("SAVE_FORMAT", "csv")

        args = {
            'url': url,
            'filename': filename,
            'save_format': save_format,
        }

        return args
