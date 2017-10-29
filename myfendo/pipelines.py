# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import codecs
from scrapy.conf import settings
import pymysql
import requests

import oss2
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class MyfendoPipeline(object):
    def __init__(self):

        self.conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='manhua', charset='utf8')
        self.cursor = self.conn.cursor()

        self.auth = oss2.Auth('LTAI6KRnoV0ZfBJH', 'VKYiSOyfZJ7ojrJZpy3u5PrCLrKWHz')
        self.bucket = oss2.Bucket(self.auth, 'oss-cn-shenzhen.aliyuncs.com', 'sayid0924')

    def process_item(self, item, spider):

        manHuna_Book_Name = item['manHuna_Book_Name']
        manHuna_Book_Type = item['manHuna_Book_Type']
        manHuna_Book_Auth = item['manHuna_Book_Auth']
        manHuna_Book_profile = item['manHuna_Book_profile']
        manHuna_Book_title = item['manHuna_Book_title']
        manHuna_Book_img_url = item['manHuna_Book_img_url']
        manHuna_Book_cover_url = item['manHuna_Book_cover_url']



        if not os.path.exists(manHuna_Book_Type):
            os.makedirs(manHuna_Book_Type)
        book_List_Ptah = os.path.abspath(manHuna_Book_Type)
        ailiyunPath ='manhua'+ "/"+manHuna_Book_Type

        conut = self.cursor.execute("select * from manhun_book_list where manhun_book_list= '%s'" % manHuna_Book_Type)

        self.cursor.fetchall()
        if conut == 0:
            sql = "insert into manhun_book_list(manhun_book_list) values(%s)"
            params = (manHuna_Book_Type)
            self.cursor.execute(sql, params)
        else:
            pass

        if not os.path.exists(manHuna_Book_Name):

           try:
             os.makedirs(book_List_Ptah + "/" + manHuna_Book_Name)
           except OSError:
             pass

        conut = self.cursor.execute("select * from manhun_book_name where manhun_book_name= '%s'" % manHuna_Book_Name)
        self.cursor.fetchall()

        book_List_Ptah = os.path.abspath(book_List_Ptah + "/" + manHuna_Book_Name)
        ailiyunPath=ailiyunPath+ "/" + manHuna_Book_Name

        if conut == 0:

            ir = requests.get(manHuna_Book_cover_url)
            if ir.status_code == 200:
                open(book_List_Ptah + "\\" + manHuna_Book_Name + '.jpg', 'wb').write(ir.content)
                imgFilePath = book_List_Ptah + "\\" + manHuna_Book_Name + '.jpg'
                ailiyunImgPath = ailiyunPath + "/" + manHuna_Book_Name + '.jpg'
                self.bucket.put_object_from_file(ailiyunImgPath, imgFilePath)

            else:
                imgFilePath = ''
                ailiyunImgPath = ''

            self.cursor.execute("select * from manhun_book_list where manhun_book_list= '%s'" % manHuna_Book_Type)
            re = self.cursor.fetchall()
            book_list_id = re[0][0]
            sql = "insert into manhun_book_name(manhun_book_name, manhun_book_list_id,book_author,book_profile,book_cover,book_cover_ailiyunImgPath) values(%s,%s,%s,%s,%s,%s)"
            params = (manHuna_Book_Name, book_list_id, manHuna_Book_Auth, manHuna_Book_profile,manHuna_Book_cover_url, ailiyunImgPath)
            self.cursor.execute(sql, params)

        else:
            pass

        if not os.path.exists(manHuna_Book_title):

           try:
                os.makedirs(book_List_Ptah + "/" + manHuna_Book_title)
           except OSError:

              pass

        book_List_Ptah = os.path.abspath(book_List_Ptah + "/" + manHuna_Book_title)
        ailiyunPath = ailiyunPath + "/" + manHuna_Book_title

        conut = self.cursor.execute("select * from manhun_book_title where manhun_book_title= '%s'" % manHuna_Book_title)
        self.cursor.fetchall()


        if conut == 0:

            self.cursor.execute("select * from manhun_book_name where manhun_book_name= '%s'" % manHuna_Book_Name)
            re = self.cursor.fetchall()
            book_list_id = re[0][0]

            sql = "insert into manhun_book_title(manhun_book_title,book_name_id) values(%s,%s)"
            params = (manHuna_Book_title,book_list_id)
            self.cursor.execute(sql, params)
        else:
            pass


        for imgurl in manHuna_Book_img_url:
            i = manHuna_Book_img_url.index(imgurl)
            ir = requests.get(imgurl)
            if ir.status_code == 200:
                open(book_List_Ptah + "\\" + str(i) + '.jpg', 'wb').write(ir.content)
                imgFilePath = book_List_Ptah + "\\" + str(i) + '.jpg'
                ailiyunImgPath = ailiyunPath + "/" + str(i) + '.jpg'
                self.bucket.put_object_from_file(ailiyunImgPath, imgFilePath)
            else:

                ailiyunImgPath=''
                imgFilePath = ''

            self.cursor.execute("select * from manhun_book_title where manhun_book_title= '%s'" % manHuna_Book_title)
            re = self.cursor.fetchall()
            book_name_id = re[0][0]
            sql = "insert into manhun_book(imgUrl, ailiyunImgPath,manhun_book_title_id) values(%s,%s,%s)"
            params = (imgurl, ailiyunImgPath, book_name_id)
            self.cursor.execute(sql, params)
        self.conn.commit()

        return item
