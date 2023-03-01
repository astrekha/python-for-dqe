import sys
import module_4 as m4
import module_5 as m5
import func_lib as fl
import os


# class for creation feed from .txt file
class TextFeed:
    def __init__(self, input_path):
        self.input_path = input_path

    def __get_file_by_path(self, input_path):
        try:
            f = open(input_path, 'r')
            f_str = f.read()
            f.close()
            return f_str
        except FileNotFoundError:
            print(f'Incorrect file path: {input_path}')

    def __get_feed_list(self, input_str):
        """
        method for getting feed lest from string
        :param input_str: str
        :return: list
        """
        try:
            output_list = []
            for part in input_str.split('***************'):
                part = part.split('\n\n')
                part = list(filter(None, part))
                output_list.append(part)
            # output_list.remove(output_list[-1])
            return output_list
        except AttributeError:
            print(f'Input string {input_str} is incorrect. __get_feed_list method cannot be applied.')

    def get_final_feed_from_txt(self, file_path_in, file_path_out):
        """
        method gets file from file_path_in or from default if file_path_in is empty, parses it,
        calculates values of publish date and day left for different feed types
        and write in appropriate format into file_path_out
        :param file_path_in: str, file_path_out str
        :return:
        """
        # tf = TextFeed(file_path_in)
        feed_str = self.__get_file_by_path(self.input_path)
        if feed_str is not None and feed_str != '':
            feed_list = self.__get_feed_list(feed_str)
            for element in feed_list:
                if element[0].lower() == 'news':
                    publication_type_in = '1'
                    publication_text_in = element[1]
                    publication_city_in = element[2]
                    news = m5.News(publication_type_in, publication_text_in, publication_city_in)
                    feed = news.format_publication(news.type, news.text, news.city, news.publish_date())
                    feed = m4.normalize_case(feed)
                    if feed is not None:
                        news.write_feed(feed, file_path_out)
                        # if file_path_in not in fl.DEFAULT_FILES:
                        #     os.remove(file_path_in)

                elif element[0].lower() == 'private ad':
                    publication_type_in = '2'
                    publication_text_in = element[1]
                    publication_exp_date_in = element[2]
                    if not fl.validate_date_format(publication_exp_date_in):
                        fl.log_error(f"Incorrect expiration date '{publication_exp_date_in}'!"
                                     f" Please,check expiration date in input file {self.input_path}.",
                                     'logs')
                        # print(f"Incorrect expiration date '{publication_exp_date_in}'!"
                        #       f" Please,check expiration date in input file {self.input_path}.")
                    else:
                        ad = m5.PrivateAd(publication_type_in, publication_text_in, publication_exp_date_in)
                        feed = ad.format_publication(ad.type, ad.text, fl.format_date(ad.exp_date),
                                                     ad.day_left(ad.exp_date))
                        feed = m4.normalize_case(feed)
                        if feed is not None:
                            ad.write_feed(feed, file_path_out)
                            # if file_path_in not in fl.DEFAULT_FILES:
                            #     os.remove(file_path_in)

                elif element[0].lower() == 'discount coupon':
                    publication_type_in = '3'
                    publication_city_in = element[1]
                    publication_text_in = element[2]
                    publication_discount_in = element[3]
                    publication_exp_date_in = element[4]
                    if not fl.validate_date_format(publication_exp_date_in):
                        # print(f"Incorrect expiration date '{publication_exp_date_in}'!"
                        #       f" Please,check expiration date in input file.")
                        fl.log_error(f"Incorrect expiration date '{publication_exp_date_in}'!"
                                     f" Please,check expiration date in input file {self.input_path}.",
                                     'logs')
                    if not fl.validate_number(publication_discount_in):
                        fl.log_error(f"Incorrect discount size '{publication_discount_in}'! "
                                     f" Please,check discount size in input file {self.input_path}.",
                                     'logs')
                        # print(f"Incorrect discount size '{publication_discount_in}'!"
                        #       f" Please,check discount size in input file.")
                    if fl.validate_date_format(publication_exp_date_in) and fl.validate_number(publication_discount_in):
                        dc = m5.DiscountCoupon(publication_type_in, publication_text_in, publication_exp_date_in,
                                               publication_discount_in, publication_city_in)
                        feed = dc.format_publication(dc.type, dc.city, dc.publish_date(), dc.text, dc.discount,
                                                     fl.format_date(dc.exp_date), dc.day_left(dc.exp_date))
                        feed = m4.normalize_case(feed)
                        if feed is not None:
                            dc.write_feed(feed, file_path_out)
                            # if file_path_in not in fl.DEFAULT_FILES:
                            #     os.remove(file_path_in)
                else:
                    print(f"Incorrect feed type '{element[0]}'")
                    fl.log_error(f"Incorrect feed type '{element[0].lower()}' in file {self.input_path}", 'logs')
            if file_path_in not in fl.DEFAULT_FILES:
                os.remove(file_path_in)
        else:
            fl.log_error(f"File {self.input_path} is empty or does not exist.", 'logs')


