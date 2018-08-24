from time import sleep
from datetime import datetime, timedelta
from abc import abstractmethod
import requests

from src.exceptions import NotTradingDate


class CrawlerBase:

    header = None

    def __init__(self, output):
        self.output = output

    def _crawl(self, url):
        """
        send a get request and get the response data

        :param url: url string
        :return: text string
        """
        try:
            res = requests.get(url)
            if not res.text:
                raise NotTradingDate

        except Exception as e:
            raise RuntimeError(str(e))

        res.encoding = 'big5'
        return res.text

    def _output(self, filename, data):
        """
        write date to output folder

        :param filename: name of output file
        :param data: output data
        """
        with open("{}/{}".format(self.output, filename), "w", encoding="utf-8") as fp:
            fp.write(data)

    def crawl(self, datetime_obj):
        """
        :param datetime_obj: datetime instance
        """
        url = self.get_url(datetime_obj)
        return self._crawl(url)

    def crawl_and_save(self, datetime_obj):
        """
        :param datetime_obj: datetime instance
        """
        filename = self.get_filename(datetime_obj)
        data = self.crawl(datetime_obj)
        self._output(filename, data)

    def crawl_by_range(self, start_date, end_date=datetime.now()):
        """
        :param start_date: start datetime object
        :param end_date: end datetime object
        """
        while start_date.date() <= end_date.date():
            date_str = start_date.strftime("%Y%m%d")
            print("Trying to get {} report ... ".format(date_str), end='')
            msg = "success"
            try:
                self.crawl_and_save(start_date)
            except (RuntimeError, NotTradingDate) as e:
                msg = "might not a trading date {}".format(str(e))
            finally:
                print(msg)
                start_date += self.interval
            sleep(5)

    @property
    def interval(self):
        return timedelta(1)

    @abstractmethod
    def get_url(self, datetime_obj):
        pass

    @abstractmethod
    def get_filename(self, datetime_obj):
        pass
