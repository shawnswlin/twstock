from datetime import datetime
from dateutil.relativedelta import relativedelta

from src.crawler.CrawlerBase import CrawlerBase


class MonthlyCrawler(CrawlerBase):
    url = "http://mops.twse.com.tw/nas/t21/sii/t21sc03_{}_{}_0.html"
    type = "html"
    base_year = 1911

    def get_url(self, datetime_obj):
        return self.url.format(datetime_obj.year - self.base_year, datetime_obj.month)

    def get_filename(self, datetime_obj):
        return "{}.{}".format(datetime_obj.strftime("%Y%m"), self.type)

    @property
    def interval(self):
        return relativedelta(months=1)

    def crawl(self, datetime_obj):
        text = super(MonthlyCrawler, self).crawl(datetime_obj)
        return "<meta charset=\"UTF-8\">\n" + text


if __name__ == "__main__":
    s_obj = datetime(2010, 1, 1)
    e_obj = datetime(2018, 7, 1)
    crawler = MonthlyCrawler("/tmp")
    print(crawler.crawl_by_range(s_obj, e_obj))
