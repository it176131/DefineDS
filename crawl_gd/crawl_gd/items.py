# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlGdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # li
    ID = scrapy.Field()
    AdvType = scrapy.Field()
    IsOrganicJob = scrapy.Field()
    AdOrderID = scrapy.Field()
    SGOCID = scrapy.Field()
    IsEasyApply = scrapy.Field()
    Title = scrapy.Field()
    Location = scrapy.Field()
    LocationID = scrapy.Field()
    LocationType = scrapy.Field()

    # li > div > a
    HREF = scrapy.Field()
    Company = scrapy.Field()

    # li > div > a > span > img
    LogoSRC = scrapy.Field()
    LogoTitle = scrapy.Field()

    # li > div > span
    CompanyRating = scrapy.Field()
