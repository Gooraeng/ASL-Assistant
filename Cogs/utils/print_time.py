from pytz import timezone
from datetime import datetime

fmt = "%Y-%m-%d %H:%M:%S"
KST = datetime.now(timezone('Asia/Seoul'))

def get_KST():
    return print(KST.strftime(fmt))