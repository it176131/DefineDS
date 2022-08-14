from scrapy import Request, Spider
from urllib.parse import urlparse
from pathlib import Path
from crawl_gd.items import CrawlGdItem


class DSSpider(Spider):
    name = "ds"

    # allowed_domains = ["glassdoor.com"]
    # start_urls = [
    #     "https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14.htm"
    # ]
    start_urls = [
        r"file:///C:\Users\A2644752\Sandbox\Medium\DefineDS\crawl_gd\html"
        r"\_Job_data-scientist-jobs-SRCH_KO0,14.htm"
    ]

    def parse(self, response, **kwargs):
        items = CrawlGdItem()
        job_listings = response.css("li[data-test='jobListing']")

        for idx, job_listing in enumerate(job_listings, start=1):
            id_ = job_listing.css("::attr(data-id)")
            items["ID"] = id_.extract()

            adv_type = job_listing.css("::attr(data-adv-type)")
            items["AdvType"] = adv_type.extract()

            is_organic_job = job_listing.css("::attr(data-is-organic-job)")
            items["IsOrganicJob"] = is_organic_job.extract()

            ad_order_id = job_listing.css("::attr(data-ad-order-id)")
            items["AdOrderID"] = ad_order_id.extract()

            sgoc_id = job_listing.css("::attr(data-sgoc-id)")
            items["SGOCID"] = sgoc_id.extract()

            is_easy_apply = job_listing.css("::attr(data-is-easy-apply)")
            items["IsEasyApply"] = is_easy_apply.extract()

            title = job_listing.css("::attr(data-normalize-job-title)")
            items["Title"] = title.extract()

            loc = job_listing.css("::attr(data-job-loc)")
            items["Location"] = loc.extract()

            loc_id = job_listing.css("::attr(data-job-loc-id)")
            items["LocationID"] = loc_id.extract()

            loc_type = job_listing.css("::attr(data-job-loc-type)")
            items["LocationType"] = loc_type.extract()

            job_listing_a = job_listing.css("div > a")

            # limit to first href with .get() instead of .extract()
            href = job_listing_a.css("::attr(href)")
            items["HREF"] = [href.get()]

            # limit to first title with .get() instead of .extract()
            company = job_listing_a.css("::attr(title)")
            items["Company"] = [company.get()]

            job_listing_img = job_listing_a.css("span > img")

            logo_src = job_listing_img.css("::attr(src)")
            items["LogoSRC"] = logo_src.extract()

            logo_title = job_listing_img.css("::attr(title)")
            items["LogoTitle"] = logo_title.extract()

            # limit to first text with .get() instead of .extract()
            rating = job_listing.css(
                "div > span[class=' job-search-key-srfzj0 e1cjmv6j0']::text"
            )
            items["CompanyRating"] = [rating.get()]

            yield items
