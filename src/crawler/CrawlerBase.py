import requests
from src.exceptions import NotTradingDate


class CrawlerBase:

    def __init__(self, output):
        self.output = output

    def _crawl(self, url):
        try:
            res = requests.get(url)
            if not res.text:
                raise NotTradingDate

        except Exception as e:
            raise RuntimeError(str(e))

        return res.text

    def _output(self, filename, data):
        with open("{}/{}".format(self.output, filename), "w", encoding="utf-8") as fp:
            fp.write(data)
