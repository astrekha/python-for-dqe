# module is used as function library for extra functions used in the application
from datetime import datetime
import os


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


def get_file_extension(file_path):
    file_extension = os.path.splitext(file_path)[1]
    return file_extension


