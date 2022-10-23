import serial
import sys
import datetime
from datetime import timezone
from datetime import datetime

def timestamp():
    dt = datetime.now()
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S"), dt.timestamp()

import time
ser = serial.Serial('COM4', 9600, timeout=None)
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=None)
buff = ""
while True:
    s = ser.read(1).decode('ascii')
    buff += s
    if s=='\n':
        date_str, ts = timestamp()
        msg = "UTC|%s|%09.3f|%s" % (date_str, ts, buff)
        sys.stdout.write(msg)
        sys.stderr.write(msg)
        sys.stdout.flush()
        buff = ""
