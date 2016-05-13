from lxml import etree
from pandas import DataFrame
import urllib
from datetime import datetime, timedelta
from electro.models import fltt
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        arrive = urllib.request.urlopen('http://192.168.5.241/inx/fltt/ajax.php?arrive&1').read()
        depart = urllib.request.urlopen('http://192.168.5.241/inx/fltt/ajax.php?depart&1').read()
        tree = etree.fromstring(arrive)
        df1 = DataFrame(columns = ['Terminal', 'TWS', 'plan', 'fact', 'num_stop'])

        for i in tree:
            dateflight = i.get('sort_1')
            time_plan = i.get('dt_plan')
            time_fact = i.get('dt_fact')
            term = i.get('term')
            tws = i.get('tws')
            num_stop = i.get('num_stop')
            try:
                time_plan = datetime.strptime(dateflight + ' ' + time_plan, '%d-%b-%y %H:%M')
            except ValueError:
                time_plan = None
            try:
                time_fact = datetime.strptime(dateflight + ' ' + time_fact, '%d-%b-%y %H:%M')
            except ValueError:
                time_fact = None
            df2 = DataFrame([[term, tws, time_plan, time_fact, num_stop]],
                            columns = ['Terminal', 'TWS', 'plan', 'fact', 'num_stop'])
            df1 = df1.append(df2, ignore_index = True)

        arr_f = df1
        stop_vs2 = ['09', '10A', '10B']
        depB = df1[(df1.Terminal == 'B') & (df1.fact >= datetime.now() - timedelta(minutes = 40))]
        depA = df1[(df1.Terminal == 'A') & (df1.fact >= datetime.now() - timedelta(minutes = 20))]
        depB3 = df1[(df1.num_stop.isin(stop_vs2)) & (df1.fact >= datetime.now() - timedelta(minutes = 40))]
        fltt.objects.update_or_create(pname = 'prilet_b', defaults = {'pznach': not depB.empty})
        fltt.objects.update_or_create(pname = 'prilet_a', defaults = {'pznach': not depA.empty})
        fltt.objects.update_or_create(pname = 'prilet_b2', defaults = {'pznach': not depB3.empty})

        tree_depart = etree.fromstring(depart)
        dep_f = DataFrame(columns = ['Terminal', 'TWS', 'plan', 'fact', 'num_stop', 'pos_beg', 'pos_end', 'reg_end'])
        for i in tree_depart:
            #     dateDepart = i.get('sdt')
            dateDepart = i.get('sort_1')
            time_plan = i.get('dt_plan')
            time_fact = i.get('dt_fact')
            pos_beg = i.get('pos_beg')
            pos_end = i.get('pos_end')
            reg_end = i.get('reg_end')
            term = i.get('term')
            tws = i.get('tws')
            num_stop = i.get('num_stop')
            try:
                time_plan = datetime.strptime(dateDepart + ' ' + time_plan, '%d-%b-%y %H:%M')
            except ValueError:
                time_plan = None
            try:
                time_fact = datetime.strptime(dateDepart + ' ' + time_fact, '%d-%b-%y %H:%M')
            except ValueError:
                time_fact = None
            try:
                pos_beg = datetime.strptime(dateDepart + ' ' + pos_beg, '%d-%b-%y %H:%M')
            except ValueError:
                pos_beg = None
            try:
                pos_end = datetime.strptime(dateDepart + ' ' + pos_end, '%d-%b-%y %H:%M')
            except ValueError:
                pos_end = None
            try:
                reg_end = datetime.strptime(dateDepart + ' ' + reg_end, '%d-%b-%y %H:%M')
            except ValueError:
                reg_end = None
            dep_f2 = DataFrame([[term, tws, time_plan, time_fact, num_stop, pos_beg, pos_end, reg_end]],
                               columns = ['Terminal', 'TWS', 'plan', 'fact', 'num_stop', 'pos_beg', 'pos_end',
                                          'reg_end'])
            dep_f = dep_f.append(dep_f2, ignore_index = True)

        stop_vs = ['07', '08', '09', '10A', '10B', '11', '12', '13', '14', '15']
        delta_minus = timedelta(minutes = 20)
        delta_plus = timedelta(minutes = 4)
        # delta_arr_minus = timedelta(minutes = 5)  # 5
        # delta_arr_plus = timedelta(minutes = 15)
        delta_dep_plan = timedelta(minutes = 45)
        time_now = datetime.now()
        arr1 = arr_f[(arr_f.num_stop.isin(stop_vs)) &
                     (arr_f.fact >= time_now - delta_minus) &
                     (arr_f.fact <= time_now + delta_plus)]
        dep1 = dep_f[(dep_f.num_stop.isin(stop_vs)) &  # стоянка ВС
                     (dep_f.fact.isnull()) &  # не улетевшие
                     (((dep_f.pos_beg <= time_now + delta_plus) &  # начало посадки <= сейчас + 4 минуты и
                       (dep_f.pos_end >= time_now - delta_minus)) |  # окончание посадки >= сейчас - 20 минут или
                      ((dep_f.plan <= time_now + delta_dep_plan) & # план вылета - 45 минут < сейчас и
                       (dep_f.plan > time_now))) # план вылета > сейчас
                      # ((dep_f.reg_end >= time_now - delta_arr_minus) &  # время регистрации >= сейчас - 5 минут и
                      #  (dep_f.reg_end < time_now + delta_arr_plus)))  # время регистрации < сейчас + 15 минут
                     ]
        bFltt = fltt.objects.all()
        for s in stop_vs:
            znach = not arr1[(arr1.num_stop == s)].empty or not dep1[(dep1.num_stop == s)].empty
            bFltt.update_or_create(pname = 'park_' + s, defaults = {'pznach': znach})
