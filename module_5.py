from datetime import datetime
from datetime import date


# basic class for feed
class Publication:
    def __init__(self, pub_type, text):
        self.type = pub_type
        self.text = text

    def get_pub_name(self, name):
        publication_types = {'1': "News", '2': "Private Ad", '3': "Discount Coupon"}
        pub_name = publication_types[name]
        return pub_name

    def format_publication(self, arg1, arg2, arg3, arg4):
        if arg1 == '1':
            publication_formatted = self.get_pub_name(arg1).title() + ' ' + '-'*25 + '\n' + \
                                    arg2 + '\n' + \
                                    arg3 + ', ' + \
                                    arg4 + '\n' + '-'*30 + '\n\n\n'
        elif arg1 == '2':
            publication_formatted = self.get_pub_name(arg1).title() + ' ' + '-'*20 + '\n' + \
                                    arg2 + '\nActual until: ' + \
                                    arg3 + ', ' + \
                                    arg4 + ' days left\n' + '-' *30 + '\n\n\n'
        else:
            publication_formatted = ''
            print(f'Incorrect value for {arg1}.')
        return publication_formatted

    def write_feed(self, feed, file_name):
        feed_file = open(file_name, "a")
        feed_file.write(feed)
        feed_file.close()


# inherited class for News
class News(Publication):
    def __init__(self, pub_type, text, city='Minsk'):
        Publication.__init__(self, pub_type=pub_type, text=text)
        self.city = city

    # encapsulation of logic for __calculate_publish_date method in publish_date method
    def publish_date(self):
        return self.__calculate_publish_date()

    # static method
    def __calculate_publish_date(self):
        return datetime.now().strftime("%d/%m/%Y %H.%M")


# inherited class for Private Ad
class PrivateAd(Publication):
    def __init__(self, pub_type, text, exp_date):
        Publication.__init__(self, pub_type=pub_type, text=text)
        self.exp_date = exp_date

    # encapsulation of logic for __calculate_day_left method in day_left method
    def day_left(self, exp_date):
        return self.__calculate_day_left(exp_date)

    # static method + encapsulation
    def __calculate_day_left(self, exp_date):
        exp_date = datetime.strptime(exp_date, '%Y-%m-%d').date()
        date_diff = str((exp_date - date.today()).days)
        return date_diff


# multi-inherited class for my feed - Discount Coupon
class DiscountCoupon(News, PrivateAd):
    def __init__(self, pub_type, text, exp_date, discount, city='Minsk'):
        News.__init__(self, pub_type=pub_type, text=text, city=city)
        PrivateAd.__init__(self, pub_type=pub_type, text=text, exp_date=exp_date)
        self.discount = discount

    # polymorphism for format_publication method
    def format_publication(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7):
        publication_formatted = self.get_pub_name(arg1).title() + ' ' + '-'*14 + '\n' + \
                                arg2 + ', ' + \
                                arg3 + '\n' + \
                                arg4 + '\nDiscount: ' + str(arg5) + \
                                '%\nActual until: ' + arg6 + ', ' + \
                                arg7 + ' days left\n' + '-'*30 + '\n\n\n'
        return publication_formatted
