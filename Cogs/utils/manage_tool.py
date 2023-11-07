# 차량 및 크럽 클래시
# Last Update : 231107

import csv
import os, sys

from Cogs.utils import settings

car_img = settings.car_img
car_list = str(settings.car_list)

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class AboutCar:        
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


class ClubClash:            
    async def Area_db():
        data  = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        data.pop(0)
        f.close()
        return data

    async def CarName_db():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[1])
        data.pop(0)
        f.close()
        return data

    async def Class_db():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[2])
        data.pop(0)
        f.close()
        return data
        
    async def LapTime_db():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[3])
        data.pop(0)
        f.close()
        return data
        
    async def Link_db():
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
