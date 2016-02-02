# -*- coding: utf-8 -*-
__author__ = 'tich'

from django.core.management.base import BaseCommand, CommandError, AppCommand
from milestone.models import MilestoneUser, MilLogin, sysSec
from datetime import datetime
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        resp = requests.post('http://192.168.16.200:5000/users')
        # resp = requests.post('http://192.168.0.140:5000/users')
        a = resp.json().pop('list')
        for i in a:
            mu, vh1 = MilestoneUser.objects.get_or_create(loginName = i['lUser'])
            ip, vh2 = sysSec.objects.get_or_create(ipAddress = i['lIP'])
            try:
                baseLogin = MilLogin.objects.get(lUser = mu, lIP = ip, lDate = datetime.strptime(i['lDate'], '%Y%m%d'))
                if baseLogin.lQuant != int(i['lQuant']):
                    baseLogin.lQuant = int(i['lQuant'])
            except MilLogin.DoesNotExist:
                b = MilLogin(lUser = mu, lIP = ip, lQuant = i['lQuant'], lDate = datetime.strptime(i['lDate'], '%Y%m%d'))
                b.save()
# self.stdout.write('Success!')