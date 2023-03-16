import module_5 as m5
import module_6 as m6
import module_7 as m7
import module_8 as m8
import module_9 as m9
import module_10 as m10
import func_lib as fl
import pyodbc


if __name__ == '__main__':

    input_info_format = input(f"Select input source:\n"
                              f"1 - Manual input from console\n"
                              f"2 - From file\n"
                              f"0 - Exit\n")

    # code block for manual input
    if input_info_format == "1":
        publication_type_in = input(f"Select publication type you want to publish:\n"
                                    f"1 - News\n"
                                    f"2 - Private Ad\n"
                                    f"3 - Discount Coupon\n")


        if publication_type_in == '1':
            publication_city_in = input("Add city: ")
            publication_text_in = input("Add text here: ")
            if publication_city_in != '':
                # creation of object of News class
                news = m5.News(publication_type_in, publication_text_in, publication_city_in)
            # getting default value for city if input is empty
            else:
                # creation of object of News class with empty city
                news = m5.News(publication_type_in, publication_text_in)
            feed = news.format_publication(type=news.type, text=news.text, city=news.city, pub_date=news.publish_date())
            # writing feed to feed.txt file
            news.write_feed(feed, "feed.txt")
            db_conn = m10.DBConnection('test.db')
            db_conn.create_table('news',
                                 'news_text text,'
                                 'news_city text, '
                                 'news_pub_date text')
            string_to_insert = db_conn.format_str_before_execute(text=news.text,
                                                                 city=news.city,
                                                                 date=news.publish_date())
            if not db_conn.is_duplicate("news", text=news.text, city=news.city):
                db_conn.insert_into_table('news', string_to_insert)
            else:
                fl.write_log_message(f"Duplicated data:'{string_to_insert}'!"
                                     f" Data will not be inserted.", 'logs')
            # print(db_conn.select_from_table('news', '*'))
            m7.write_word_statistics('feed.txt')
            m7.write_letter_statistics('feed.txt')
            print(f"Database data in table 'news' is: {db_conn.select_from_table('news', '*')}")
        elif publication_type_in == '2':
            publication_exp_date_in = input("Add expiration date in YYYY-MM-DD format: ")
            # validation of input expiration date
            while not fl.validate_date_format(publication_exp_date_in):
                print(f"Incorrect expiration date '{publication_exp_date_in}'! "
                      f"Please, re-enter expiration date.")
                publication_exp_date_in = input("Add expiration date in YYYY-MM-DD format: ")
            publication_text_in = input("Add text here: ")
            # creation of object of PrivateAd class
            ad = m5.PrivateAd(publication_type_in, publication_text_in, publication_exp_date_in)
            feed = ad.format_publication(type=ad.type, text=ad.text, exp_date=fl.format_date(ad.exp_date),
                                         day_left=ad.day_left(ad.exp_date))
            # writing feed to feed.txt file
            ad.write_feed(feed, "feed.txt")
            db_conn = m10.DBConnection('test.db')
            db_conn.create_table('private_ad',
                                 'ad_text text, '
                                 'ad_exp_date text,'
                                 'ad_day_left integer')
            string_to_insert = db_conn.format_str_before_execute(text=ad.text,
                                                                 exp_date=ad.exp_date,
                                                                 day_left=ad.day_left(ad.exp_date))
            if not db_conn.is_duplicate("private_ad", text=ad.text, exp_date=ad.exp_date):
                db_conn.insert_into_table('private_ad', string_to_insert)
            else:
                fl.write_log_message(f"Duplicated data:'{string_to_insert}'!"
                                     f" Data will not be inserted.", 'logs')
            print(f"Database data in table 'private_ad' is: {db_conn.select_from_table('private_ad', '*')}")
            m7.write_word_statistics('feed.txt')
            m7.write_letter_statistics('feed.txt')
        elif publication_type_in == '3':
            publication_city_in = input("Add city: ")
            publication_text_in = input("Add text here: ")
            publication_exp_date_in = input("Add expiration date in YYYY-MM-DD format: ")
            # validation of input expiration date
            while not fl.validate_date_format(publication_exp_date_in):
                print(f"Incorrect expiration date '{publication_exp_date_in}'! "
                      f"Please, re-enter expiration date.")
                publication_exp_date_in = input("Add expiration date in YYYY-MM-DD format: ")
            publication_discount_in = input("Add discount size in %: ")
            # validation of input discount size
            while not fl.validate_number(publication_discount_in):
                print(f"Incorrect discount size '{publication_discount_in}'!"
                      f" Please,re-enter discount size.")
                publication_discount_in = input("Add discount size in %: ")
            if publication_city_in != '':
                # creation of object of DiscountCoupon class
                dc = m5.DiscountCoupon(publication_type_in, publication_text_in,
                                       publication_exp_date_in, publication_discount_in, publication_city_in)
            else:
                # getting default value for city if input is empty
                dc = m5.DiscountCoupon(publication_type_in, publication_text_in,
                                       publication_exp_date_in, publication_discount_in)
            feed = dc.format_publication(type=dc.type, city=dc.city, pub_date=dc.publish_date(), text=dc.text,
                                         discount=dc.discount, exp_date=fl.format_date(dc.exp_date),
                                         day_left=dc.day_left(dc.exp_date))
            # writing feed to feed.txt file
            dc.write_feed(feed, "feed.txt")
            db_conn = m10.DBConnection('test.db')
            db_conn.create_table('discount_coupon',
                                 'dc_text text, '
                                 'dc_city text, '
                                 'dc_pub_date text, '
                                 'dc_exp_date text, '
                                 'dc_discount real, '
                                 'dc_day_left integer')
            string_to_insert = db_conn.format_str_before_execute(text=dc.text,
                                                                 city=dc.city,
                                                                 pub_date=dc.publish_date(),
                                                                 exp_date=dc.exp_date,
                                                                 discount=dc.discount,
                                                                 day_left=dc.day_left(dc.exp_date)
                                                                 )
            if not db_conn.is_duplicate("discount_coupon",
                                        text=dc.text, city=dc.city,
                                        exp_date=dc.exp_date, discount=dc.discount):
                db_conn.insert_into_table('discount_coupon', string_to_insert)
            else:
                fl.write_log_message(f"Duplicated data:'{string_to_insert}'!"
                                     f" Data will not be inserted.", 'logs')
            print(f"Database data in table 'discount_coupon' is: {db_conn.select_from_table('discount_coupon', '*')}")
            m7.write_word_statistics('feed.txt')
            m7.write_letter_statistics('feed.txt')

        else:
            print(f'"{publication_type_in}" type of publication is incorrect!')

    # code block for input from file
    elif input_info_format == "2":
        file_extension = input("Provide file extension you want to use: ")
        file_path = input("Provide path to file you want to use: ")
        if file_extension == '.txt':
            # taking default .txt file in case of empty input path
            if file_path == '':
                parsed_arg = fl.add_default_files()
                file_path = parsed_arg[1]
            # creation of object of TextFeed class
            tf = m6.TextFeed(file_path)
            # calling a method for getting feed from txt file
            tf.get_final_feed_from_txt(file_path, 'feed.txt')
            # writing statistics files for words and letters
            m7.write_word_statistics('feed.txt')
            m7.write_letter_statistics('feed.txt')
            db = m10.DBConnection('test.db')
            try:
                print(f'Table \'news\' contains data: {db.select_from_table("news", "*")}')
            except pyodbc.Error:
                print(f'Table \'news\' does not exist.')
            try:
                print(f'Table \'private_ad\' contains data: {db.select_from_table("private_ad", "*")}')
            except pyodbc.Error:
                print(f'Table \'private_ad\' does not exist.')
            try:
                print(f'Table \'discount_coupon\' contains data: {db.select_from_table("discount_coupon", "*")}')
            except pyodbc.Error:
                print(f'Table \'discount_coupon\' does not exist.')
            # draft for next modules
        elif file_extension == '.json':
            # taking default .json file in case of empty input path
            if file_path == '':
                parsed_arg = fl.add_default_files()
                file_path = parsed_arg[2]
            # creation of object of JsonFeed class
            jf = m8.JsonFeed(file_path)
            # calling a method for getting feed from json file
            jf.get_final_feed_from_json(file_path, 'feed.txt')
            # writing statistics files for words and letters
            m7.write_word_statistics('feed.txt')
            m7.write_letter_statistics('feed.txt')
            db = m10.DBConnection('test.db')
            try:
                print(f'Table \'news\' contains data: {db.select_from_table("news", "*")}')
            except pyodbc.Error:
                print(f'Table \'news\' does not exist.')
            try:
                print(f'Table \'private_ad\' contains data: {db.select_from_table("private_ad", "*")}')
            except pyodbc.Error:
                print(f'Table \'private_ad\' does not exist.')
            try:
                print(f'Table \'discount_coupon\' contains data: {db.select_from_table("discount_coupon", "*")}')
            except pyodbc.Error:
                print(f'Table \'discount_coupon\' does not exist.')
        elif file_extension == '.xml':
            # taking default .json file in case of empty input path
            if file_path == '':
                parsed_arg = fl.add_default_files()
                file_path = parsed_arg[3]
            # creation of object of JsonFeed class
            xf = m9.XmlFeed(file_path)
            # calling a method for getting feed from json file
            xf.get_final_feed_from_xml(file_path, 'feed.txt')
            # writing statistics files for words and letters
            m7.write_word_statistics('feed.txt')
            m7.write_letter_statistics('feed.txt')
            db = m10.DBConnection('test.db')
            try:
                print(f'Table \'news\' contains data: {db.select_from_table("news", "*")}')
            except pyodbc.Error:
                print(f'Table \'news\' does not exist.')
            try:
                print(f'Table \'private_ad\' contains data: {db.select_from_table("private_ad", "*")}')
            except pyodbc.Error:
                print(f'Table \'private_ad\' does not exist.')
            try:
                print(f'Table \'discount_coupon\' contains data: {db.select_from_table("discount_coupon", "*")}')
            except pyodbc.Error:
                print(f'Table \'discount_coupon\' does not exist.')
        else:
            print(f'Incorrect file extension {file_extension}!')
    elif input_info_format == "0":
        exit(0)
    else:
        print("Input source is incorrect")

