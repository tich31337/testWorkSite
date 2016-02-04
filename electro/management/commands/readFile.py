# -*- coding: utf-8 -*-
__author__ = 'tich'


from django.core.management.base import BaseCommand, CommandError, AppCommand
from electro.models import energosfera, nameCount
from datetime import datetime
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        resp = open('/home/tich/worksite/electro/scet.csv', encoding = 'windows-1251')
        # resp = requests.post('http://192.168.16.200:5000/users')
        # resp = requests.post('http://192.168.0.140:5000/users')
        for i in resp:
            a = i.split(';')
            nameCount.objects.create(nCount = str(a[0]), nId = int(a[1]))
            print('ok')
