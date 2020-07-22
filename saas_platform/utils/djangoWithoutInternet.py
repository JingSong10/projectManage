import os
import sys

import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas_platform.settings")
django.setup()
from web import models

models.Userinfo.objects.create(username="zhangsan", email="123@123.com", mobile_phone=15552217716, password="111111")

