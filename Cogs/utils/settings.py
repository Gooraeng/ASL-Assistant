# 디코 세팅
# Last Update : 231113

import os, sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

load_dotenv()

discord_api_token = os.getenv('discord_api_token')
list_url = os.getenv('list_url')
car_list = os.getenv('car_list')
car_img = os.getenv('car_img')
mei = os.getenv('mei')
a9_db = os.getenv('a9_db')
log_channel = os.getenv('log_channel')
feedback_log_channel = os.getenv('feedback_log_channel')
ASL_Assistant_owner_id = os.getenv('ASL_Assistant_owner_id')