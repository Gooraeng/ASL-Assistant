from pytz import timezone
from datetime import datetime

fmt = "%Y-%m-%d %H:%M:%S"
KST_time = datetime.utcnow(timezone('Asia/Seoul'))

def get_KST():
    return KST_time.strftime(fmt)