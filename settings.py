# 디코 세팅
# 민감한 파일

import os
from dotenv import load_dotenv

load_dotenv

token = os.getenv('discord_api_token')
list_url = os.getenv('list_url')
check_diff = os.getenv('check_diff_reference')