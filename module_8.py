import sys
import module_4 as m4
import module_5 as m5
import func_lib as fl
import os
import json as j
from json.decoder import JSONDecodeError


# class for creation feed from .json file
class JsonFeed:
    def __init__(self, input_path):
        self.input_path = input_path

    def __get_file_by_path(self, input_path):
        try:
            with open(input_path, 'r') as f:
                f_str = j.load(f)
                f.close()
                return f_str
        except FileNotFoundError:
            print(f'Incorrect file path: {input_path}')
        except JSONDecodeError:
            print(f'Incorrect json structure or file is empty: {input_path}')

    def get_final_feed_from_json(self, file_path_in, file_path_out):
        """
        method gets file from file_path_in or from default if file_path_in is empty, parses it,
        calculates values of publish date and day left for different feed types
        and write in appropriate format into file_path_out
        :param file_path_in: str, file_path_out str
        :return:
        """
        # if file_path_in == '':
        #     file_path_in = sys.argv[0]
        # jf = JsonFeed(file_path_in)
        feed_list = self.__get_file_by_path(self.input_path)
        if feed_list is not None and feed_list != '':
            is_file_valid = True
            for element in feed_list:
                if element["type"].lower() == 'news':
                    publication_type_in = '1'
                    publication_text_in = element["text"]
                    publication_city_in = element["city"]
                    news = m5.News(publication_type_in, publication_text_in, publication_city_in)
                    feed = news.format_publication(type=news.type, text=news.text, city=news.city,
                                                   pub_date=news.publish_date())
                    feed = m4.normalize_case(feed)
                    if feed is not None:
                        news.write_feed(feed, file_path_out)
                        # if file_path_in not in fl.DEFAULT_FILES:
                        #     os.remove(file_path_in)
                elif element["type"].lower() == 'private ad':
                    publication_type_in = '2'
                    publication_text_in = element["text"]
                    publication_exp_date_in = element["exp_date"]
                    if not fl.validate_date_format(publication_exp_date_in):
                        # print(f"Incorrect expiration date '{publication_exp_date_in}'!"
                        #       f" Please,check expiration date in input file.")
                        is_file_valid = False
                        fl.write_log_message(f"Incorrect expiration date '{publication_exp_date_in}'!"
                                             f" Please,check expiration date in input file {self.input_path}.",
                                             'logs')
                    else:
                        ad = m5.PrivateAd(publication_type_in, publication_text_in, publication_exp_date_in)
                        feed = ad.format_publication(type=ad.type, text=ad.text, exp_date=fl.format_date(ad.exp_date),
                                                     day_left=ad.day_left(ad.exp_date))
                        feed = m4.normalize_case(feed)
                        if feed is not None:
                            ad.write_feed(feed, file_path_out)
                            # if file_path_in not in fl.DEFAULT_FILES:
                            #     os.remove(file_path_in)
                elif element["type"].lower() == 'discount coupon':
                    publication_type_in = '3'
                    publication_city_in = element["city"]
                    publication_text_in = element["text"]
                    publication_discount_in = element["discount"]
                    publication_exp_date_in = element["exp_date"]
                    if not fl.validate_date_format(publication_exp_date_in):
                        # print(f"Incorrect expiration date '{publication_exp_date_in}'!"
                        #       f" Please,check expiration date in input file.")
                        is_file_valid = False
                        fl.write_log_message(f"Incorrect expiration date '{publication_exp_date_in}'!"
                                             f" Please,check expiration date in input file {self.input_path}.",
                                             'logs')
                    if not fl.validate_number(publication_discount_in):
                        # print(f"Incorrect discount size '{publication_discount_in}'!"
                        #       f" Please,check discount size in input file.")
                        is_file_valid = False
                        fl.write_log_message(f"Incorrect discount size '{publication_discount_in}'! "
                                             f" Please,check discount size in input file {self.input_path}.",
                                             'logs')
                    if fl.validate_date_format(publication_exp_date_in) and fl.validate_number(publication_discount_in):
                        dc = m5.DiscountCoupon(publication_type_in, publication_text_in, publication_exp_date_in,
                                               publication_discount_in, publication_city_in)
                        feed = dc.format_publication(type=dc.type, city=dc.city, pub_date=dc.publish_date(),
                                                     text=dc.text, discount=dc.discount,
                                                     exp_date=fl.format_date(dc.exp_date),
                                                     day_left=dc.day_left(dc.exp_date))
                        feed = m4.normalize_case(feed)
                        if feed is not None:
                            dc.write_feed(feed, file_path_out)
                            # if file_path_in not in fl.DEFAULT_FILES:
                            #     os.remove(file_path_in)
                else:
                    print(f'Incorrect feed type {element["type"]}')
                    fl.write_log_message(f'Incorrect feed type \"{element["type"]}\" in file {self.input_path}', 'logs')
            if is_file_valid and file_path_in not in fl.DEFAULT_FILES:
                fl.write_log_message(f"f File {file_path_in} successfully processed and will be removed", 'logs')
                os.remove(file_path_in)
        else:
            fl.write_log_message(f"File {self.input_path} is empty, has incorrect structure or does not exist.", 'logs')
