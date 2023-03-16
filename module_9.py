import module_4 as m4
import module_5 as m5
import module_10 as m10
import func_lib as fl
import os
import xml.etree.ElementTree as et


# class for creation feed from .xml file
class XmlFeed:
    def __init__(self, input_path):
        self.input_path = input_path

    def __get_file_by_path(self, input_path):
        try:
            tree = et.parse(input_path)
            root = tree.getroot()
            return root
        except FileNotFoundError:
            print(f'Incorrect file path: {input_path}')
        except et.ParseError:
            print(f'Incorrect json structure in: {input_path}')



    def get_final_feed_from_xml(self, file_path_in, file_path_out):
        """
        method gets file from file_path_in or from default if file_path_in is empty, parses it,
        calculates values of publish date and day left for different feed types
        and write in appropriate format into file_path_out
        :param file_path_in: str, file_path_out str
        :return:
        """
        feed_list = self.__get_file_by_path(self.input_path)
        if feed_list is not None and feed_list != '':
            is_file_valid = True
            for element in feed_list:
                if element.attrib["type"].lower() == 'news':
                    publication_type_in = '1'
                    publication_text_in = element.find('text').text
                    publication_city_in = element.find('city').text
                    news = m5.News(publication_type_in, publication_text_in, publication_city_in)
                    feed = news.format_publication(type=news.type, text=news.text, city=news.city,
                                                   pub_date=news.publish_date())
                    feed = m4.normalize_case(feed)
                    if feed is not None:
                        db_conn = m10.DBConnection('test.db')
                        db_conn.create_table('news',
                                             'news_text text, '
                                             'news_city text, '
                                             'news_pub_date text')
                        string_to_insert = db_conn.format_str_before_execute(text=m4.normalize_case(news.text),
                                                                             city=m4.normalize_case(news.city),
                                                                             date=news.publish_date())
                        # print(db_conn.is_duplicate("news", text=news.text, city=news.city))

                        if not db_conn.is_duplicate("news", text=news.text, city=news.city):
                            db_conn.insert_into_table('news', string_to_insert)
                            news.write_feed(feed, file_path_out)
                        else:
                            fl.write_log_message(f"Duplicated data:'{string_to_insert}'!"
                                                 f" Data will not be inserted.", 'logs')
                elif element.attrib["type"].lower() == 'private ad':
                    publication_type_in = '2'
                    publication_text_in = element.find("text").text
                    publication_exp_date_in = element.find("exp_date").text
                    if not fl.validate_date_format(publication_exp_date_in):
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
                            db_conn = m10.DBConnection('test.db')
                            db_conn.create_table('private_ad',
                                                 'ad_text text, '
                                                 'ad_exp_date text, '
                                                 'ad_day_left integer')
                            string_to_insert = db_conn.format_str_before_execute(text=m4.normalize_case(ad.text),
                                                                                 exp_date=fl.format_date(
                                                                                     ad.exp_date),
                                                                                 day_left=ad.day_left(ad.exp_date))
                            if not db_conn.is_duplicate("private_ad", text=ad.text,
                                                        exp_date=fl.format_date(ad.exp_date)):
                                db_conn.insert_into_table('private_ad', string_to_insert)
                                ad.write_feed(feed, file_path_out)
                            else:
                                fl.write_log_message(f"Duplicated data:'{string_to_insert}'!"
                                                     f" Data will not be inserted.", 'logs')
                elif element.attrib["type"].lower() == 'discount coupon':
                    publication_type_in = '3'
                    publication_city_in = element.find("city").text
                    publication_text_in = element.find("text").text
                    publication_discount_in = element.find("discount").text
                    publication_exp_date_in = element.find("exp_date").text
                    if not fl.validate_date_format(publication_exp_date_in):
                        is_file_valid = False
                        fl.write_log_message(f"Incorrect expiration date '{publication_exp_date_in}'!"
                                             f" Please,check expiration date in input file {self.input_path}.",
                                             'logs')
                    if not fl.validate_number(publication_discount_in):
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
                            db_conn = m10.DBConnection('test.db')
                            db_conn.create_table('discount_coupon',
                                                 'dc_text text, '
                                                 'dc_city text, '
                                                 'dc_pub_date text, '
                                                 'dc_exp_date text, '
                                                 'dc_discount real, '
                                                 'dc_day_left integer')
                            string_to_insert = db_conn.format_str_before_execute(text=m4.normalize_case(dc.text),
                                                                                 city=m4.normalize_case(dc.city),
                                                                                 pub_date=dc.publish_date(),
                                                                                 exp_date=fl.format_date(
                                                                                     dc.exp_date),
                                                                                 discount=dc.discount,
                                                                                 day_left=dc.day_left(dc.exp_date)
                                                                                 )
                            if not db_conn.is_duplicate("discount_coupon",
                                                        text=dc.text, city=dc.city,
                                                        exp_date=fl.format_date(dc.exp_date), discount=dc.discount):
                                db_conn.insert_into_table('discount_coupon', string_to_insert)
                                dc.write_feed(feed, file_path_out)
                            else:
                                fl.write_log_message(f"Duplicated data:'{string_to_insert}'!"
                                                     f" Data will not be inserted.", 'logs')
                else:
                    print(f'Incorrect feed type {element.attrib["type"]}')
                    fl.write_log_message(f'Incorrect feed type \"{element.attrib["type"]}\" in file {self.input_path}', 'logs')
            if is_file_valid and file_path_in not in fl.DEFAULT_FILES:
                fl.write_log_message(f"File {file_path_in} successfully processed and will be removed", 'logs')
                os.remove(file_path_in)
        else:
            fl.write_log_message(f"File {self.input_path} is empty, has incorrect structure or does not exist.", 'logs')
