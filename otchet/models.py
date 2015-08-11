# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser, User, UserManager
from django.utils.translation import ugettext_lazy as _

class CustomUser(User):
    class Meta:
        verbose_name='Пользователь'
        verbose_name_plural='Пользователи'

    # def __str__(self):
    #     self.p_num

    birthday    = models.DateField          (_('birthday')      , blank = True, null = True                     )
    p_num       = models.SmallIntegerField  ('Табельный номер'  , blank=True, null=True                         )
    patronymic  = models.CharField          ('Отчество'         , max_length=50, blank=True, null=True          )
    group       = models.ForeignKey         ('s_group'          , verbose_name='Группа', blank=True, null=True  )
    office      = models.ForeignKey         ('s_office'         , verbose_name='Должность', blank=True, null=True)
    timetable   = models.ForeignKey         ('s_timetable'      , verbose_name='График работы', blank=True, null=True )
    telephone   = models.CharField          ('Телефон'          , max_length=15, blank=True, null=True          )
    fired       = models.BooleanField       ('Уволен'           , default=False                                 )
    objects     = UserManager()

class s_group(models.Model):

    class Meta:
        verbose_name        = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.group_name

    group_name = models.CharField('Название группы', max_length=150)

class s_office(models.Model):

    class Meta:
        verbose_name        = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return self.office_name
    
    office_name = models.CharField      ('Должность', max_length=50        )
    group       = models.ManyToManyField('s_group'  , verbose_name='Группа')
    
class s_timetable(models.Model):

    class Meta:
        verbose_name        = "График работы"
        verbose_name_plural = "График работы"

    def __str__(self):
        return self.smena
    
    smena = models.CharField('Смена', max_length=10)    

class s_system(models.Model):

    class Meta:
        verbose_name        = "Система"
        verbose_name_plural = "Системы"
        ordering            = ['system_name']

    def __str__(self):
        return self.system_name
    
    system_name = models.CharField  ('Название системы', max_length=50                      )
    group       = models.ForeignKey ('s_group'         , verbose_name='Ответственная группа')    

class s_fault(models.Model):
    
    class Meta:
        verbose_name        = "Происшествие"
        verbose_name_plural = "Происшествия"
        ordering            = ['fault_time']

    def __str__(self):
        return '%s - %s %s %s %s' % (self.fault_time, self.f_system, self.s_object, self.description, self.correction)
    
    fault_time  = models.DateTimeField  (              verbose_name='Время'       )
    f_staff     = models.ForeignKey     ('CustomUser', verbose_name='Пользователь')
    f_system    = models.ForeignKey     ('s_system'  , verbose_name='Система'     )
    s_object    = models.ForeignKey     ('s_objects' , verbose_name='Объект'      )
    description = models.CharField      ('Описание'  , max_length=500             )
    correction  = models.BooleanField   ('Устранено' , default=False              )

# Падения с лифтов эскалаторов, либо остановка

class s_drop_lift(models.Model):

    class Meta:
        verbose_name        = "Остановка лифта (эскалатора)"
        verbose_name_plural = "Остановка лифтов (эскалаторов)/падения"
        ordering            = ['stop_lift']

    def __str__(self):
        return '%s - %s %s %s %s' % (self.stop_lift, self.start_lift, self.lift_name, self.fault, self.description)
    
    stop_lift   = models.DateTimeField  (verbose_name ='Время остановки'            )
    start_lift  = models.DateTimeField  ('Время запуска', blank=True, null=True     )
    lift_name   = models.ForeignKey     ('s_lift'       , verbose_name='Название'   )
    fault       = models.ForeignKey     ('s_fault_lift' , verbose_name='Происшествие'        )
    description = models.CharField      ('Описание'     , max_length=50, blank=True )
    consequences= models.BooleanField   ('Без последствий'                          )

class s_lift(models.Model):

    class Meta:
        verbose_name        = "Лифт/Эскалатор"
        verbose_name_plural = "Лифты/Эскалаторы"
        ordering            = ['ser_num']

    def __str__(self):
        return '%s %s %s %s' % (self.get_terminal_display(), self.get_l_type_display(), self.ser_num, self.location)

    LIFT_CHOICES = (
        ('Л', 'Лифт'        ),
        ('Э', 'Эскалатор'   ),
        )

    TERMINAL_CHOICES = (
        ('A', 'Терминал A'),
        ('B', 'Терминал B'),
        )

    ser_num     = models.SmallIntegerField  ('Номер'                                                                            )
    l_type      = models.CharField          ('Тип'                                    , max_length=1, choices = LIFT_CHOICES    )
    terminal    = models.CharField          ('Терминал'                               , max_length=1, choices = TERMINAL_CHOICES)
    location    = models.CharField          ('Месторасположение, направление, этаж'   , max_length=50                           )

class s_fault_lift(models.Model):

    class Meta:
        verbose_name        = "Причина остановки"
        verbose_name_plural = "Причины остановки"

    def __str__(self):
        return self.type_fault
    
    type_fault = models.CharField('Причины остановки', max_length=50)

class s_objects(models.Model):

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    name    = models.CharField      ('Название объекта' , max_length=150                    )
    system  = models.ManyToManyField('s_system'         , verbose_name='Системы', blank=True)

    # TODO: сделать поле ответственный за пожарную безопасность fk т. всех пользователей, автоматически формировать акты проверки систем.

class s_commit(models.Model):

    class Meta:
        verbose_name = "Сдача отчета"
        verbose_name_plural = "Сдача отчета"

    def __str__(self):
        return '%s %s' % (self.s_time, self.s_staff_commit,) 

    s_time = models.DateTimeField(verbose_name='Время сдачи отчета')    
    s_fault_commit = models.ForeignKey('s_fault', verbose_name = 'Последний коммит (сбои)')
    s_lift_commit = models.ForeignKey('s_drop_lift', verbose_name = 'Последний коммит (лифты)')
    s_prim = models.TextField(verbose_name='Примечание', blank='True', null='True')
    s_staff_commit = models.ForeignKey('CustomUser')