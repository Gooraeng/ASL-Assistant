from pytz import timezone
from datetime import datetime

fmt = "%Y-%m-%d %H:%M:%S"
KST_time = datetime.now(timezone('Asia/Seoul'))

def get_KST():
    KST_time.strftime(fmt)