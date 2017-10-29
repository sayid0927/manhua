# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyfendoItem(scrapy.Item):
    # define the fields for your item here like:
    manHuna_Book_Name = scrapy.Field()
    manHuna_Book_Type = scrapy.Field()
    manHuna_Book_Auth = scrapy.Field()
    manHuna_Book_profile = scrapy.Field()
    manHuna_Book_title = scrapy.Field()
    manHuna_Book_img_url = scrapy.Field()
    manHuna_Book_cover_url = scrapy.Field()