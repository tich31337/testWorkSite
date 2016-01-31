# -*- coding: utf-8 -*-
__author__ = 'tich'

from django.contrib import admin
from .models import MilestoneUser, MilLogin, sysSec

admin.site.register(MilestoneUser)
admin.site.register(MilLogin)
admin.site.register(sysSec)
