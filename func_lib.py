# module is used as function library for extra functions used in the application
from datetime import datetime
import sys

DEFAULT_FILES = ['input_file.txt', 'input_file.json']

def format_date(date):
    try:
        date_formatted = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        print(f"Incorrect input date format: {date}")
        date_formatted = ''
    return date_formatted


def validate_date_format(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_number(discount):
    try:
        discount = float(discount)
        return True
    except ValueError:
        return False


def add_default_files():
    parsed_arg = sys.argv.copy()
    for f in DEFAULT_FILES:
        parsed_arg.append(f)
    return parsed_arg

