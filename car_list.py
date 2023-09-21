# 차량 리스트 만들기 위한 함수 임포트
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml
import csv
import settings
import os

class Managing():
    async def make_a9_car_list():
        url = settings.list_url
    
        response = requests.get(url).text.encode('utf-8')
        response = BeautifulSoup(response, 'lxml')
    
        target = response.find('table',{'id':'list', 'class':'table'})
        thead = target.find_all('th')
    
        theadList = []
    
        theadLen = len(thead)
        for i in range(0, theadLen):
            thead = target.find_all('th')[i].text
            theadList.append(thead)

        tdTags = target.find_all('td')

        rowList=[]
        columnList = []

        tdTagsLen = len(tdTags)
        for i in range(0, tdTagsLen):
            element = tdTags[i].text
            columnList.append(element)
            if i % 2 ==1:
                rowList.append(columnList)
                columnList=[]
        result = pd.DataFrame(rowList,columns=theadList)
        print(result)
    
        f = open(settings.the_csv,'w',encoding='utf-8',newline='')
        writer = csv.writer(f)
        writer.writerows(rowList)
        f.close()
        
    
    async def check_uptate():
        data = list()
        f = open(settings.the_csv, "r",encoding='utf-8')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        f.close()
        
        car_img_list = list()
        for filename in os.listdir("Car_spec_img"):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                car_img_list.append(filename[:-4])
            elif filename.endswith(".jpeg"):
                car_img_list.append(filename[:-5])
        
        check_new = list(set(data)- set(car_img_list))

        if set(data) == set(car_img_list):
            if check_new is None:
                print('추가된 차량이 없습니다!')
        else:
            if 'KTM  X-BOW GTX' in data:
                print('추가된 차량이 없습니다!')
            else:
                print('차량 업데이트 발견: '+ str(check_new))