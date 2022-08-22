import json
from scrapy import Request, Spider
from urllib.parse import urlparse
from pathlib import Path
from crawl_gd.items import CrawlJobListingItem, CrawJobDescriptionItem


class JobListingSpider(Spider):
    name = "listing"

    allowed_domains = ["glassdoor.com"]
    start_urls = [
        "https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14.htm"
    ]
    # start_urls = [
    #     r"file:///C:\Users\A2644752\Sandbox\Medium\DefineDS\crawl_gd\html"
    #     r"\_Job_data-scientist-jobs-SRCH_KO0,14.htm"
    # ]

    def parse(self, response, **kwargs):
        """"""
        items = CrawlJobListingItem()
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

            urgency = job_listing.css("div[data-test='urgency-label']::text")
            items["Urgency"] = urgency.extract()

            age = job_listing.css("div[data-test='job-age']::text")
            items["Age"] = age.extract()

            salary_est = job_listing.css(
                "span[data-test='detailSalary']::text"
            )
            items["SalaryEstimate"] = salary_est.extract()

            salary_est_type = job_listing.css(
                "span[data-test='detailSalary'] > span::text"
            )
            items["SalaryEstimateType"] = salary_est_type.extract()

            yield items

        next_page_url = self.get_next_page_url(response)

        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

    def get_next_page_url(self, response):
        """Find and navigate to next page if available"""
        # what page are we on
        current_page_str = response.css(
            "button[class='page selected css-1hq9k8 e13qs2071']"
            "::attr(data-test)"
        ).get()
        current_page_list = current_page_str.split("-")
        current_page_number = int(current_page_list[-1])

        # determine max page count
        page_range_text = response.css(
            "div[class='paginationFooter']::text"
        ).get()
        page_range = page_range_text.split()
        max_page_str = page_range[-1]
        max_page_number = int(max_page_str)

        # can we go further?
        if current_page_number < max_page_number:
            next_page_number = current_page_number + 1
            next_page_url = f"https://www.glassdoor.com/Job/data-scientist" \
                            f"-jobs-SRCH_KO0,14_IP{next_page_number}.htm"
            return next_page_url

        return None


class JobDescriptionSpider(Spider):
    """"""

    name = "description"

    allowed_domains = ["glassdoor.com"]

    def __init__(self, *args, **kwargs):
        self._get_start_urls()
        super().__init__(*args, **kwargs)

    def _get_start_urls(self):
        """"""
        job_listings_path = Path.cwd() / "html" / "job_listings.json"
        with job_listings_path.open(mode="rb") as f:
            job_listings = json.load(fp=f)

        for job_listing in job_listings:
            href_list = job_listing.get("HREF")
            href = href_list[0]

            if href:
                job_listing_url = f"{self.allowed_domains[0]}{href}"
                self.start_urls.append(job_listing_url)

    def parse(self, response, **kwargs):
        """"""
        items = CrawJobDescriptionItem()

        description = response.css(
            "div[id='JobDescriptionContainer'] > div > div > div"
        )

        items["Description"] = description.getall()
