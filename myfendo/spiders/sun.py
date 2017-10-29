# -*- coding: utf-8 -*-
import re
import urllib2

import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from myfendo.items import MyfendoItem

from downloader import Downloader

from myfendo.spiders.hh import download


class SunSpider(CrawlSpider):
    name = 'sun'
    home_url='http://comic.sfacg.com'
    allowed_domains = ['comic.sfacg.com']
    start_urls = ['http://comic.sfacg.com/Catalog/?tid=2']

    # rules = (
    #     Rule(LinkExtractor(allow=r'list/\d+.html'), process_links = "deal_links", callback='parse_item'),
    #     # Rule(LinkExtractor(allow=r'\d+')),
    #     # Rule(LinkExtractor(allow=r'book/\d+/\d+/\d+.html'), callback='parse_item'),
    # )
    #
    # http: // comic.sfacg.com / Catalog /?tid = 1

    # def deal_links(self, links):
    #     for each in links:
    #         print(each)
    #         # each.url = each.url.replace("?", "&").replace("Type&", "Type?")
    #     return links



    URL = 'http://comic.sfacg.com'
    picture = 'http://coldpic.sfacg.com'

    def parse(self, response):

        manHuan_list = response.xpath('//li[@class="Conjunction"]//@href').extract()
        manHuan_nex_list = response.xpath('//ul[@class="nav pagebar"]/li/a/@href').extract()

        if len(manHuan_nex_list):

            for Nex_Url in manHuan_nex_list:
                yield scrapy.Request(Nex_Url, callback=self.parse)
        else:
            print ('manHuan_nex_list is NULL')

        if len(manHuan_list):
            for Info_Url in manHuan_list:
                yield scrapy.Request(Info_Url, callback=self.manHuan_Info)
        else:
            print ("manHuan_list is NULL")


    def manHuan_Info(self, response):

        # 书名
        manHuna_Book_Name=response.xpath('//td[@class="font_gray gray_link1"]//span/text()').extract()[0]
        # 类型
        manHuna_Book_Type = response.xpath('//ul[@class="Height_px22"]//a/text()').extract()[0]
        # 作者
        manHuna_Book_Auth = response.xpath('//ul[@class="Height_px22"]//a/text()').extract()[1]
        # 简介
        manHuna_Book_profile = response.xpath('//ul[@class="Height_px22"]/li/text()').extract()[4]
        # 书title
        manHuna_Book_title_url = response.xpath('//ul[@class="serialise_list Blue_link2"]//a/@href').extract()
        # 书头像
        manHuna_Book_cover_url = response.xpath('//td[@class="comic_cover"]/img/@src').extract()[0]


        # 书名是否为空
        if manHuna_Book_Name.strip() == '':
            print 'manHuna_Book_Type is null'
            manHuna_Book_Name= 'null'
        else:
            manHuna_Book_Name= manHuna_Book_Name

        # 书类型是否为空
        if manHuna_Book_Type.strip() == '':
            print 'manHuna_Book_Type is null'
            manHuna_Book_Type='null'
        else:
            manHuna_Book_Type = manHuna_Book_Type

        # 书作者是否为空
        if manHuna_Book_Auth.strip() == '':
            print 'manHuna_Book_Auth is null'
            manHuna_Book_Auth = 'null'
        else:
            manHuna_Book_Auth = manHuna_Book_Auth

        # 书简介是否为空
        if manHuna_Book_profile.strip() == '':
            print 'manHuna_Book_profile is null'
            manHuna_Book_profile='null'
        else:
            manHuna_Book_profile = manHuna_Book_profile

        # 书头像是否为空
        if manHuna_Book_cover_url.strip() == '':
             print 'manHuna_Book_cover_url is null'
             manHuna_Book_cover_url = 'null'
        else:
            manHuna_Book_cover_url = manHuna_Book_cover_url




        if len(manHuna_Book_title_url):
            for Info_Url in manHuna_Book_title_url:
                title_url= self.home_url+Info_Url
                yield scrapy.Request(title_url,meta={'manHuna_Book_cover_url':manHuna_Book_cover_url,'manHuna_Book_Name':manHuna_Book_Name,'manHuna_Book_Type': manHuna_Book_Type,'manHuna_Book_Auth': manHuna_Book_Auth,'manHuna_Book_profile': manHuna_Book_profile},callback=self.manHuan_Title)
        else:
            print 'manHuna_Book_title_url is null'



    def manHuan_Title(self, response):

        manHuna_Book_Name = response.meta['manHuna_Book_Name']
        manHuna_Book_Type = response.meta['manHuna_Book_Type']
        manHuna_Book_Auth = response.meta['manHuna_Book_Auth']
        manHuna_Book_profile = response.meta['manHuna_Book_profile']
        manHuna_Book_cover_url = response.meta['manHuna_Book_cover_url']



        # 书标题
        manHuna_Book_title = response.xpath('//div[@class="wrap"]/span/text()').extract()[0]

        manHuna_Book_img_url = self.get_section_page(response.url)

        # # 图片URL
        # manHuna_Book_img_url = response.xpath('//td[@valign="top"]/a/img/@src').extract()
        # # 下一张图片url
        # manHuna_Book_title_next_url = response.xpath('//div[@class="page_turning AD_D3"]//a/@href').extract()




        # 书标题是否为空
        if manHuna_Book_title.strip() == '':
            print 'manHuna_Book_title is null'
            manHuna_Book_title = 'null'
        else:
            manHuna_Book_title = manHuna_Book_title

        i = MyfendoItem()

        i['manHuna_Book_Name'] = manHuna_Book_Name
        i['manHuna_Book_Type'] = manHuna_Book_Type
        i['manHuna_Book_Auth'] = manHuna_Book_Auth
        i['manHuna_Book_profile'] = manHuna_Book_profile
        i['manHuna_Book_title'] = manHuna_Book_title
        i['manHuna_Book_img_url'] = manHuna_Book_img_url
        i['manHuna_Book_cover_url'] = manHuna_Book_cover_url


        yield i






    # def book_list(self, response):
    #     links = response.xpath('//strong[@class="F14PX"]//a/@href').extract()
    #
    #     book_List = response.meta['book_List']
    #     for link in links:
    #         i = links.index(link)
    #         yield scrapy.Request(link, meta={'href_url': link, 'book_List': book_List}, callback=self.book_href)
    #
    # def book_href(self, response):
    #
    #     links = response.xpath(
    #         "//div[@class='comic_Serial_list']//a/@href | //ul[@class='serialise_list Blue_link2']//a/@href").extract()
    #     book_auth = response.xpath('//ul[@class="Height_px22"]/li').extract()
    #
    #     book_cover = response.xpath('//td[@class="comic_cover"]/img/@src').extract()[0]
    #
    #     book_List = response.meta['book_List']
    #     href_url = response.meta['href_url']
    #
    #     for link in links:
    #         count = re.sub("\D", "", link)
    #         url = href_url + count
    #         yield scrapy.Request(url, meta={'book_cover':book_cover,'book_List': book_List, 'book_auth': book_auth}, callback=self.process_item)
    #
    # def process_item(self, response):
    #
    #     book_title = response.xpath('//div[@class="wrap"]//span/text()').extract()[0]
    #     imgUrlList = self.get_section_page(response.url)
    #     book_info = response.meta['book_auth']
    #     book_cover = response.meta['book_cover']
    #     book_auth = book_info[1]
    #     book_profile = book_info[4]
    #     book_List = response.meta['book_List']
    #
    #     book_auth = book_auth.replace('<li>', "").replace('</li>', "").replace('<a>', "").replace('</a>', "")
    #     book_auth = book_auth.split('<')
    #     auth = book_auth[0]
    #     book_auth = book_auth[1]
    #     book_auth = book_auth.split('>')
    #     book_auth = auth + book_auth[1]
    #
    #     book_profile = book_profile.replace('<li>', "").replace('</li>', "")
    #     book_profile = book_profile.split('<a')[0]
    #
    #     book_name = book_title[0:book_title.rfind(re.sub("\D", "", book_title))]
    #
    #     i = MyfendoItem()
    #
    #     i['bookname'] = book_name
    #     i['imgUrlList'] = imgUrlList
    #     i['book_auth'] = book_auth
    #     i['book_profile'] = book_profile
    #     i['book_title'] = book_title
    #     i['book_List'] = book_List
    #     i['book_cover'] = book_cover
    #
    #
    #     yield i
    #
    #
    def download(url, user_agent='wswp', num_try=2):

        headers = {'User_agent': user_agent}
        request = urllib2.Request(url, headers=headers)
        try:
            html = urllib2.urlopen(request).read()
        except urllib2.URLError as e:
            print 'Download error', e.reason
            html = None
            if num_try > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return download(url, user_agent, num_try - 1)
                elif e.code == 403:
                    return None
        return html

    def get_section_page(self, url):

        html = self.download(url)
        if html == None:
            return None
        soup = BeautifulSoup(html, "html.parser")
        results = soup.find_all(name='script', attrs={'type': 'text/javascript'})
        tt = len(results)
        js = results[tt - 1]
        mm = js.get('src')
        if mm == None:
            result = soup.find_all(name='script', attrs={'language': 'javascript'})
            js1 = result[1]
            mm = js1.get('src')
        html1 = self.download(self.URL + mm)
        List = []
        if html1 :
            list = html1.split(';')
            List = []
            for each in list:
                if 'picAy[' in each:
                    src = each.split('=')
                    List.append(self.picture + src[1][2:-1])
        else:
            return None

        return List

    def download(self,url, user_agent='wswp', num_try=2):

        headers = {'User_agent': user_agent}
        request = urllib2.Request(url, headers=headers)
        try:
            html = urllib2.urlopen(request).read()
        except urllib2.URLError as e:
            print 'Download error', e.reason
            html = None
            if num_try > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.download(url, user_agent, num_try - 1)
                elif e.code == 403:
                    return None
        return html
