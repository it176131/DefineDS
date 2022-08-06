from scrapy import Request, Spider
from urllib.parse import urlparse
from pathlib import Path


class DSSpider(Spider):
    name = "ds"

    allowed_domains = ["glassdoor.com"]
    start_urls = [
        "https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14.htm"
    ]

    def parse(self, response, **kwargs):
        # save html --> don't want to make multiple requests when building
        url = response.url
        parsed_url = urlparse(url=url)
        url_path = parsed_url.path
        file_name = url_path.replace("/", "_")

        html_dir = Path.cwd() / "html"
        html_dir.mkdir(parents=True, exist_ok=True)

        with open(html_dir / file_name, mode="wb") as file:
            file.write(response.body)
