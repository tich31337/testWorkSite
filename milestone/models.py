# -*- coding: utf-8 -*-
__author__ = 'tich'

from django.db import models
from datetime import date, timedelta


class MilestoneUser(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.loginName

    firstName = models.CharField('Имя', max_length = 50, blank = True, null = True)
    patroName = models.CharField('Отчество', max_length=50, blank = True, null = True)
    lastName = models.CharField('Фамилия', max_length = 50, blank = True, null = True)
    loginName = models.CharField('Логин', max_length=50)
    
class sysSec(models.Model):
	
    class Meta:
        verbose_name        = 'Система'
        verbose_name_plural = 'Системы'

    def __str__(self):
        return self.ipAddress

    ipAddress = models.GenericIPAddressField(unique = True)
    sysName = models.CharField('Название', max_length=50, blank = True, null = True)
    description = models.CharField('Описание', max_length=50, blank = True, null = True)
    milUser = models.ForeignKey('MilestoneUser', blank = True, null = True, verbose_name = 'Пользователь Milestone')
    miAdmin = models.BooleanField(verbose_name = 'Администратор Milestone', default = False)

class MilLogin(models.Model):

    class Meta:
        verbose_name        = 'Milestone Login'
        verbose_name_plural = 'Milestone Login'
        permissions = (('can_read_ml', 'Может читать'),)

    def __str__(self):
        return str(self.lUser) +' ' + str(self.lIP)+ ' ' + str(self.lDate)

    lUser = models.ForeignKey('MilestoneUser')
    lIP = models.ForeignKey('sysSec')
    lQuant = models.IntegerField()
    # lDate = models.DateField(default = date.today()-timedelta(1))
    lDate = models.DateField()


class MilCamera(models.Model):

    class Meta:
        verbose_name        = 'Камера'
        verbose_name_plural = 'Камера'
        permissions = (('can_read_ml', 'Может читать'),)
        ordering = ('CameraName',)

    def __str__(self):
        return str(self.CameraName)

    ipAddress = models.GenericIPAddressField(blank = True, null = True)
    CameraName = models.CharField('Название', max_length=150)


class MilLogin2(models.Model):

    class Meta:
        verbose_name        = 'Пользователь'
        verbose_name_plural = 'Пользователь'
        permissions = (('can_read_ml', 'Может читать'),)
        ordering = ('mUser',)

    def __str__(self):
        return str(self.mUser)

    mUser = models.CharField('Пользователь', max_length=50)
    mCameras = models.ManyToManyField(MilCamera)
    mDate = models.DateField()
