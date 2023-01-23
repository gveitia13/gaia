from django.test import TestCase

import datetime
import pytz

spain_timezone = pytz.timezone("Europe/Madrid")
spain_time = datetime.datetime.now(spain_timezone)
print(spain_time)

