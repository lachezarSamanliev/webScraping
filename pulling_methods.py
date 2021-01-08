import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium import webdriver
import time
import os
from extmysql import db_helper

class maker:

    def __init__(self):
        self.db_reach = db_helper()

    def get_page(self, url):
        r = requests.get(url)
        html = r.text
        soup_now = BeautifulSoup(html, "html.parser")
        return soup_now


    def put_data(self, date_received, province, project, investor, link_page):
        query_three = "INSERT IGNORE INTO razreshitelni_tb (date_received, province, project, investor, link_page) VALUES (%s, %s, %s, %s, %s)"
        data = (date_received, province, project, investor, link_page)
        self.db_reach.execute(query_three, data)

    def get_data(self, province):
        ##Cases will be in switch I guess
        ## switch result is based on province name
        if province == 'varna':
            url_page = 'https://agup.varna.bg/index.php/registers/2013-04-23-07-00-18/razresheniya-za-stroezh-2020-g-2'
            province_name = 'Варна'
            dat = self.get_page(url_page)
            #make list for the three fields
            dati = []
            type_obekt = []
            investor = []
            linkove = []
            #here we get date published
            sisterstuff = dat.find_all(class_='ari-tbl-col-0')

            for tag in sisterstuff:
                temp_one = tag.text.strip()
                ss = temp_one.split('/')
                if not(len(ss) < 2):
                #if len(ss) = 2:
                    dati.append(ss[1])
                    #print(ss[1])
            #now get the second column
            second_column = dat.find_all(class_='ari-tbl-col-1')
            for tag_two in second_column:
                #print(tag_two.text.strip())
                temp_two = tag_two.text.strip()
                if len(temp_two) > 10:
                    type_obekt.append(temp_two)
            #get third column
            third_column = dat.find_all(class_='ari-tbl-col-2')
            for tag_three in third_column:
                #print(tag_three.text.strip())
                temp_three = tag_three.text.strip()
                if not(temp_three == 'възложител'):
                    if len(temp_three) >2:
                        investor.append(temp_three)
                        linkove.append("empty")

            #reversing list
            investor.reverse()
            type_obekt.reverse()
            dati.reverse()
            limit = len(dati)
            for inserter in range(0,limit):
                self.put_data(dati[inserter], province_name, type_obekt[inserter], investor[inserter], linkove[inserter])
                #print('inserted')


        elif province == "plovdiv":
            url_page = 'https://pd.government.bg/?page_id=9996'

            province_name = 'Пловдив'
            substr_one = 'РАЗРЕШАВАМ'
            substr_two = 'Относно:'
            dat = self.get_page(url_page)
            #make list for the three fields
            dati = []
            type_obekt = []
            investor = []
            linkove = []
            temp_type_obekt = []
            #here we get date published
            split_one= dat.find_all(class_='su-post-title')
            for tag in split_one:
                temp_one = tag.text.strip()
                #print(temp_one)
                ss = temp_one.split('/')
                if not(len(ss) < 2):
                    dati.append(ss[1])
            #now get the second column
            split_two = dat.find_all(class_='su-post-excerpt')
            for tag_two in split_two:
                temp_two = tag_two.text.strip()

                #print(temp_two)
                if substr_one in temp_two:
                    #split it up
                    res_one = temp_two.split('теля ')
                    res_two = res_one[1].split('№')

                    #THIS IS INVESTOR NAME
                    investor.append(res_two[0])

                    #THIS IS TYPE OF BUILD
                    get_type = res_two[1].split('г. ')
                    #print(get_type)
                    #Some might be missed I guess.
                    try:
                        get_type = res_two[1].split('г. ')
                        type_obekt.append(get_type[1])
                    except:
                        print("this broke")
                        get_type = res_two[1].split('извърши ')
                        type_obekt.append(get_type[1])

                elif substr_two in temp_two:
                    inv_name = temp_two.split('на ',1)
                    investor.append(inv_name[1])
                    temp_type_obekt.append('няма информация')

            split_three = dat.find_all(class_='su-post-view')
            for tag_three in split_three:
                temp_three = tag_three
                opit = str(temp_three)
                #print(opit)
                #now only get the link somehow
                split_one = opit.split('href="')
                split_two = split_one[1].split('" title')
                #print(split_two[0])
#append link list
                linkove.append(split_two[0])

                #print("space")

            print(dati)
            print(investor)
            print(type_obekt)
            print(linkove)
            print(len(dati))
            print(len(investor))
            print(len(type_obekt))
            print(len(linkove))
            ##PUT IN DATABASE WITH LOOP
        elif province == "sofia":
            url_page = 'https://www.sofia-agk.com/RegisterBuildingPermitsPortal/Index'
            province_name = 'София'

            first_part_link = 'https://www.sofia-agk.com/RegisterInfo/Info?url='
            #just add jGJRUdJV1zo= from third instance

            dati = []
            type_obekt = []
            investor = []
            linkove = []

            driver = webdriver.Chrome(r"C:\Users\lsama\Desktop\ushemi\chromedriver_win32\chromedriver")
            driver.get(url_page)
            time.sleep(5)

            html = driver.page_source
            soupp = BeautifulSoup(html, 'lxml')
            #print(soupp)
            for tag in soupp.find_all("tbody"):
                #print(tag.text)
                trying = tag.text
                som = str(trying)
                som2 = som.splitlines()
                y = [s for s in som2 if len(s) > 5]
                dati_temp_one = []
                print (y)
                for we in [0,6,12,18,24,30,36,40,46,52]:
                    try:
                        print(y[we])
                        date_split = y[we].split("/")
                        dati_temp_one.append(date_split[1])
                        #print('dati')
                    except:
                        print("I broke " + str(we))

                dati_temp_two = []
                for we_two in [3,9,15,21,27,33,39,45,51,57]:
                    try:
                        print(y[we_two])
                        #get link
                        for_link_split = y[we_two].split('=')
                        linkove.append(str(first_part_link + for_link_split[0] + '='))
                        #get data
                        data_here = for_link_split[1].split(' г.')
                        dati_temp_two.append(data_here[0])


                        #get Vuzlojitel
                        temp_vuzlojitel = data_here[1]
                        investor.append(temp_vuzlojitel)
                        #print("more data")
                    except:
                        print("I broke two " + str(we_two))

                for we_three in [4,10,16,22,28,34,40,46,52,58]:
                    try:
                        #get type_obekt
                        temp_obekt = y[we_three]
                        type_obekt.append(temp_obekt)
                        #print('type obekt')
                    except:
                        print("I broke three " + str(we_three))
                #some for loop to make them go to the next line
                #separate steps for cleaning I guess
                for i in range (0,len(dati_temp_one)):
                    dati.append(dati_temp_one[i] + dati_temp_two[i])

                # 0 = date
                # 3 = link + date_released + investor
                # 4 = type_obekt
                # total_range = len(y)
                # range = len(y) / 6
                # for we in range(0, len(y), 6):
                #     #here we get items and append.
                #     date_split = y[we].split("/")
                #     date_temp = date_split[1].rstrip()
                #     dati.append(date_temp)
                #
                # #for we_two in range(3,)
                # print(dati)
                #print(y)
                limit = len(dati)
                for inserter in range(0,limit):
                    try:
                        self.put_data(dati[inserter], province_name, type_obekt[inserter], investor[inserter], linkove[inserter])
                        print("yes")
                    except:
                        print("no")
                print("space")

        elif province == "blagoevgrad":
            print("dd")
        elif province == "shumen":
            url_page = 'https://www.shumen.bg/ustrojstvo-na-teritoriyata/razresheniya-za-stroezh/'
            province_name = 'Шумен'



            r = requests.get(url_page)
            html = r
            html.encoding = 'utf-8'
            soup_here = BeautifulSoup(html.text, 'html.parser')
            #dat = self.get_page(url_page)
            #make list for the three fields
            dati = []
            type_obekt = []
            investor = []

            #here links will be empty.
            linkove = []
            #here we get date published
            #print(soup_here)
            #temp_hold = dat.find("div", attrs={"class":"wpb_wrapper"})
            #sisterstuff = zip(soup_here.find_all(class_='wpb_wrapper'), soup_here.find_all("p", attrs={"style":"text-align:"}))
            release_dates = []
            sisterstuff = soup_here.find_all('p', {'style': 'text-align: right;'})
            for tag in sisterstuff:
                date = tag.text.strip()
                release_dates.append(date)
                #print(date)
                #print("space")

            temp_two = soup_here.find_all('p', {'style': 'text-align: justify;'})
            substr_one = 'за строеж'
            for tag in temp_two:
                sega = tag.text.strip()
                split_one = sega.split(substr_one)
                print(split_one)
                print("TWOO TWOO")
                split_two = split_one[1].split(' от ')
                print(split_two)
                split_three = split_two[1].split('г')

                #print(sega)
                print("OOOOOOOOOOOOOOOOOOO")
                print(split_three)


        elif province == "burgas":
            url_page = "https://www.burgas.bg/bg/notice/index/61/0"
            province_name = 'Бургас'
            substring = 'издадено разрешение за  строеж'
            substring_two = 'издадено разрешение за строеж'

            dati = []
            type_obekt = []
            investor = []
            linkove = []

            dat = self.get_page(url_page)
            temp_one = dat.find_all(class_='media-body')

            for tag in temp_one:
                temp_clean = tag.text.strip()
                separated = temp_clean.splitlines()

                print("space")
                if ((substring_two in separated[0]) or (substring_two in separated[2])):
                    print("found")
                    #print(separated)
                    #get link
                    temp_tag = tag
                    link_split = str(temp_tag)
                    link_split_one = link_split.split('a href="')
                    link_split_two = link_split_one[1].split('"><')
                    #print(link_split_two[0])
                    linkove.append(link_split_two[0])
                    #here work on splitting and getting info
                    #inside [2] look for date and type obekt
                    try:
                        split_one = separated[2].split(substring_two)
                    #    print(split_one)
                        split_two = split_one[1].split(' от ')
                    #    print(split_two)
                        split_three = split_two[1].split('г. за обект')
                    #    print(split_three)
                        dati.append(split_three[0])
                        type_obekt.append(split_three[1])
                        investor.append('empty')
                    except:
                        print("it broke")
                    #print(split_two)

                if((substring in separated[2]) or substring in separated[0]):
                    print("here found")
                    temp_tag = tag
                    link_split = str(temp_tag)
                    link_split_one = link_split.split('a href="')
                    link_split_two = link_split_one[1].split('"><')
                    #print(link_split_two[0])
                    linkove.append(link_split_two[0])
                    try:

                        split_one = separated[2].split(substring_two)
                        split_two = split_one[1].split(' от ')
                        split_three = split_two[1].split(' за обект')
                    #    print(split_three)
                        dati.append(split_three[0])
                        type_obekt.append(split_three[1])
                        investor.append('empty')
                    except:
                        print("broke it")
                        #split it up
                        # res_one = temp_two.split('теля ')
                        # res_two = res_one[1].split('№')

            print(dati)
            print(linkove)
            print(investor)
            print(type_obekt)
            limit = len(dati)
            for inserter in range(0,limit):
                self.put_data(dati[inserter], province_name, type_obekt[inserter], investor[inserter], linkove[inserter])





        #result = self.db_reach.fetch("SELECT title FROM upvotes_db")

## PUT NAME OF CITY INSIDE prov VARIABLE TO CHANGE THE METHOD EXECUTION.
mak = maker()
prov = 'burgas'
mak.get_data(prov)

