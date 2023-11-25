# 디코 세팅
# Last Update : 231113

import os, sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

load_dotenv()

discord_api_token = os.getenv('discord_api_token')
log_channel = os.getenv('log_channel')
feedback_log_channel = os.getenv('feedback_log_channel')
ASL_Assistant_owner_id = os.getenv('ASL_Assistant_owner_id')
twip_donate_log_channel = os.getenv('twip_donate_log_channel')