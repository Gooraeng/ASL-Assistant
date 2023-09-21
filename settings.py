import os
from dotenv import load_dotenv

load_dotenv

token = os.getenv('discord_api_token')
list_url = os.getenv('list_url')
the_csv = os.getenv('the_csv')
check_diff = os.getenv('check_diff_reference')