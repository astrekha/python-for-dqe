import pyodbc
import re


class DBConnection:
    def __init__(self, database_name):
        with pyodbc.connect('DRIVER={SQLite3 ODBC Driver};'
                            f'Database={database_name}') as self.connection:
            self.cursor = self.connection.cursor()

    def create_table(self, table_name, field_def):
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({field_def})')

    def insert_into_table(self, table_name, value):
        self.cursor.execute(f'INSERT INTO {table_name} VALUES({value})')
        self.cursor.commit()

    def select_from_table(self, table_name, field):
        self.cursor.execute(f'SELECT {field} FROM {table_name} ')
        return self.cursor.fetchall()

    def format_str_before_execute(self, **kwargs):
        string = ''
        for k in kwargs.keys():
            string = string + "'" + str(kwargs[k]).replace("'", "''") + "'" + ','
        return string[:len(string)-1]

    def is_duplicate(self, table_name, **kwargs):
        sql = ''
        backslash_char_n = "\n"
        backslash_char_t = "\t"
        formatted_text = str(self.format_str_before_execute(text=kwargs["text"]))
        formatted_text = formatted_text.replace(backslash_char_n, " ")
        formatted_text = formatted_text.replace(backslash_char_t, " ")
        formatted_text = re.sub(' +', ' ', formatted_text)
        if table_name == 'news':
            sql = (f'SELECT count(*) '
                   f'FROM {table_name} '
                   f'where lower(replace(news_text,char(10)," ")) = '
                   f'lower({formatted_text})'
                   f' and '
                   f'lower(news_city) = lower({self.format_str_before_execute(city=kwargs["city"])})')
        elif table_name == 'private_ad':
            sql = (f'SELECT count(*) '
                   f'FROM {table_name} '
                   f'where lower(replace(ad_text,char(10)," ")) = '
                   f'lower({formatted_text})'
                   f' and '
                   f'ad_exp_date = {self.format_str_before_execute(exp_date=kwargs["exp_date"])}')
        elif table_name == 'discount_coupon':
            sql = (f'SELECT count(*) '
                   f'FROM {table_name} '
                   f'where lower(replace(dc_text,char(10)," ")) = '
                   f'lower({formatted_text})'
                   f' and '
                   f'lower(dc_city) = lower({self.format_str_before_execute(city=kwargs["city"])})'
                   f' and '
                   f'dc_exp_date = {self.format_str_before_execute(exp_date=kwargs["exp_date"])}'
                   f' and '
                   f'dc_discount = {self.format_str_before_execute(discount=kwargs["discount"])}')
        # return sql
        self.cursor.execute(sql)
        if self.cursor.fetchall()[0][0] != 0:
            return True
        else:
            return False
