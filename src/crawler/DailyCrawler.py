from datetime import datetime, timedelta
from time import sleep

from src.crawler.CrawlerBase import CrawlerBase
from src.exceptions import NotTradingDate


class DailyCrawler(CrawlerBase):
    url = "http://www.tse.com.tw/exchangeReport/MI_INDEX?type=ALLBUT0999&date={}&response={}"
    default_type = "csv"

    def crawl(self, date_str, file_type=default_type):
        """
        :param date_str: date string likes 20100101
        :param file_type: csv or json
        """
        url = self.url.format(date_str, file_type)
        return self._crawl(url)

    def crawl_and_save(self, date_str):
        """
        :param date_str: date string likes 20100101
        """
        filename = "{}.{}".format(date_str, self.default_type)
        data = self.crawl(date_str)
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
                self.crawl_and_save(date_str)
            except (RuntimeError, NotTradingDate):
                msg = "might not a trading date"
            finally:
                print(msg)
                start_date += timedelta(1)
            sleep(5)


if __name__ == "__main__":
    # date_string = "20100105"
    # crawler = DailyCrawler("/tmp")

    date_obj = datetime(2010, 1, 1)
    crawler = DailyCrawler("/tmp")
    print(crawler.crawl_by_range(date_obj))
