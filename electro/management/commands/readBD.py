# -*- coding: utf-8 -*-
__author__ = 'tich'

from django.core.management.base import BaseCommand, CommandError, AppCommand
from electro.models import energosfera, nameCount
from datetime import datetime
import os, re, pytz
import requests
def convertDate(*args):
    dateI = ''
    for i in args:
        i = str(i)
        if len(i) == 1:
            i = '0'+i
        dateI += i
    return datetime.strptime(dateI, '%Y%m%d%H')

class Command(BaseCommand):


    def handle(self, *args, **options):
        resp = open(os.getcwd()+'/electro/2016 часовые.csv', encoding = 'utf-8')
        # resp = open('/home/tich/worksite/electro/scet.csv', encoding = 'windows-1251')
        # resp = requests.post('http://192.168.16.200:5000/users')
        # resp = requests.post('http://192.168.0.140:5000/users')
        v = 0
        energosfera.objects.all().delete()
        for i in resp:
            # v +=1
            a = i.split(';')
            a[5] = float(re.sub(',','.',re.sub(r'\n','',str(a[5]))))
            b = nameCount.objects.get(nId = a[0])
            # ,tzinfo=pytz.timezone('Etc/GMT+5')
            d = datetime(int(a[1]),int(a[2]),int(a[3]),int(a[4]))
            # print(d)
            energosfera.objects.create(eId= b, eDate = d, ekwt = a[5])
            # if v == 1000:
            #     break