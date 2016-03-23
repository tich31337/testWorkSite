from lxml import etree
from pandas import DataFrame
import urllib
from datetime import datetime, timedelta
from electro.models import fltt
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        arrive = urllib.request.urlopen('http://192.168.5.241/inx/fltt/ajax.php?arrive&1').read()
        tree = etree.fromstring(arrive)
        df1 = DataFrame(columns=['Terminal', 'fact'])
        for i in tree:
            dateflight = i.get('sort_1')
            time_fact = i.get('dt_fact')
            term = i.get('term')
            try:
                time_fact = datetime.strptime(dateflight+' '+time_fact, '%d-%b-%y %H:%M')
            except ValueError:
                time_fact = None
            df2 = DataFrame([[term, time_fact]], columns=['Terminal', 'fact'])
            df1 = df1.append(df2, ignore_index = True)

        # df1 = df1[(df1.Terminal == 'B') & (df1.plan < pd.datetime.now()+datetime.timedelta(minutes = 120))\
        #           & (df1.plan >= pd.datetime.now()-datetime.timedelta(minutes = 220))]
        df1 = df1[(df1.Terminal == 'B')  & (df1.fact >= datetime.now()-timedelta(minutes = 40))]
        if df1.empty:
            arr = False
        else:
            arr = True
        # print(arr)
        pril = fltt.objects.get(pname = 'prilet_b')
        pril.pznach = arr
        pril.save()