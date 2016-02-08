from django.db import models
from otchet.models import s_objects
# Create your models here.

class energosfera(models.Model):

    class Meta:
        verbose_name        = 'Потребление'
        verbose_name_plural = 'Потребление'
        ordering = ['eDate', 'eId']
        permissions = (('can_read_electro', 'Потребление'),)

    def __str__(self):
        return '{} {} {} кВт'.format(self.eDate, self.eId, self.ekwt)

    ekwt = models.FloatField(verbose_name = 'Потребление',)
    eId = models.ForeignKey('nameCount',verbose_name = 'Счетчик')
    eDate = models.DateTimeField(verbose_name = 'Время',)
    
class nameCount(models.Model):
	
    class Meta:
        verbose_name        = 'Счетчик'
        verbose_name_plural = 'Счетчик'
        ordering = ['nBuild','nCount',]

    def __str__(self):
        return '{0} {1} {2}'.format(self.nBuild, self.nCount, self.nId,)

    nCount = models.CharField('Название', max_length=50)
    nId = models.IntegerField(verbose_name = 'Идентификатор', unique = True)
    nBuild = models.ForeignKey('otchet.s_objects',verbose_name = 'Объект', blank = True, null = True)
