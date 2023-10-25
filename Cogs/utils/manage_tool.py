import settings
from bs4 import BeautifulSoup as beau
import requests as req
import csv
import os, sys
import pandas as pd

car_img = settings.car_img
car_list = str(settings.car_list)

class AboutCar:
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        
    async def make_new_car_list():
        url = str(settings.list_url)

        response = req.get(url).text.encode('utf-8')
        response = beau(response, 'lxml')

        target = response.find('table',{'id':'list', 'class':'table'})
        thead = target.find_all('th')

        theadList = []

    # 사이트 내 th, td 태그 제거 
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
        result = pd.DataFrame(rowList, columns=theadList)
        
    # 태그 제거 결과 확인
        print(result)

        # csv 파일로 우선 저장 [차량, 클래스] 꼴로 저장됨
        f = open(car_list,'w',encoding='utf-8',newline='')
        writer = csv.writer(f)
        writer.writerow(theadList)
        writer.writerows(rowList)
        f.close()

        return result

    async def utilize_list():
        data = list()
        f = open('data/A9 Car List.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        data.pop(0)
        f.close()
        return data

    async def make_car_img_list():
        car_img_list  = list()
        for filename in os.listdir('Car_spec_img'):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                car_img_list.append(filename[:-4])
            elif filename.endswith(".jpeg"):
                car_img_list.append(filename[:-5])
        return car_img_list


            
    async def ClubClash_Database_area():
        data  = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        data.pop(0)
        f.close()
        return data

    async def ClubClash_Database_CarName():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[1])
        data.pop(0)
        f.close()
        return data

    async def ClubClash_Database_Class():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[2])
        data.pop(0)
        f.close()
        return data
        
    async def ClubClash_Database_LapTime():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[3])
        data.pop(0)
        f.close()
        return data
        
    async def ClubClash_Database_Link():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[4])
        data.pop(0)
        f.close()
        return data


async def check_update():
    data_csv = await AboutCar.utilize_list() 
    data_img = await AboutCar.make_car_img_list()
    
# 업데이트 된 차량(들)의 리스트 선언 
    check_new = list(set(data_csv)- set(data_img))
    if len(list(data_csv))-len(list(data_img))==0:
        if 'KTM  X-BOW GTX' in data_csv:
            return check_new == None
    else:
        if 'KTM  X-BOW GTX' in data_csv:
            check_new.remove('KTM  X-BOW GTX')
            return check_new
            
async def print_CP():

    await AboutCar.make_new_car_list()
    data_csv = await AboutCar.utilize_list() 
    data_img = await AboutCar.make_car_img_list()

    # 업데이트 된 차량(들)의 리스트 선언 
    check_new = list(set(data_csv)- set(data_img))
    
    # 리스트 대조 후 일치 시
    # KTM X-BOW GTX는 이미 존재하는 차량인데 data 리스트에서는 띄어쓰기가 두 번 적용된 것이 확인되어 억지로 맞게 만듬
    if len(list(data_csv))-len(list(data_img))==0:
        if 'KTM  X-BOW GTX' in data_csv:
            return print('추가된 차량이 없습니다!')

    # 리스트 대조 후 불일치 시
    # 89번 줄과 같은 사유
    else:
        if 'KTM  X-BOW GTX' in data_csv:
            check_new.remove('KTM  X-BOW GTX')
            return print('차량 업데이트 발견: '+ str(check_new))
