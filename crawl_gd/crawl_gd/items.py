# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlJobListingItem(scrapy.Item):
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
    HREF = scrapy.Field()
    Company = scrapy.Field()
    LogoSRC = scrapy.Field()
    LogoTitle = scrapy.Field()
    CompanyRating = scrapy.Field()
    Urgency = scrapy.Field()
    Age = scrapy.Field()
    SalaryEstimate = scrapy.Field()
    SalaryEstimateType = scrapy.Field()


class CrawJobDescriptionItem(scrapy.Item):
    Description = scrapy.Field()
    Salary = scrapy.Field()
    Company = scrapy.Field()
    Rating = scrapy.Field()
