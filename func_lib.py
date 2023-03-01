# module is used as function library for extra functions used in the application
from datetime import datetime
import sys
import os

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


def log_error(in_error_msg, out_file_path):
    out_file_name = datetime.now().strftime("%Y_%m_%d" + '_error_log.txt')
    full_file_path = os.path.join(out_file_path, out_file_name)
    log_file = open(full_file_path, "a")
    log_file.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + ' Error: ' + in_error_msg + '\n')
    log_file.close()
