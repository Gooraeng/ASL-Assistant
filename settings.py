# 디코 세팅
# 민감한 파일

import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('discord_api_token')
list_url = os.getenv('list_url')
car_list = os.getenv('car_list')
club_clash_database = os.getenv('club_clash_database')
car_img = os.getenv('car_img')
mei = os.getenv('mei')
a9_db = os.getenv('a9_db')