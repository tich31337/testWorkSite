# -*- coding: utf-8 -*-
__author__ = 'tich'

from django.contrib import admin
from .models import MilestoneUser, MilLogin, sysSec, MilCamera, MilLogin2

admin.site.register(MilestoneUser)
admin.site.register(MilLogin)
admin.site.register(sysSec)
admin.site.register(MilCamera)
admin.site.register(MilLogin2)
