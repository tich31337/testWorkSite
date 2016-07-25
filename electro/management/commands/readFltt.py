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
        arrive1 = DataFrame(columns = ['Terminal', 'TWS', 'ap', 'plan', 'fact', 'num_stop'])

        for i in tree:
            dateflight = i.get('sort_1')
            time_plan = i.get('dt_plan')
            time_fact = i.get('dt_fact')
            term = i.get('term')
            tws = i.get('tws')
            ap = i.get('ap')
            num_stop = i.get('num_stop')
            try:
                time_plan = datetime.strptime(dateflight + ' ' + time_plan, '%d-%b-%y %H:%M')
            except ValueError:
                time_plan = None
            try:
                time_fact = datetime.strptime(dateflight + ' ' + time_fact, '%d-%b-%y %H:%M')
            except ValueError:
                time_fact = None
            arrive_temp = DataFrame([[term, tws, ap, time_plan, time_fact, num_stop]],
                            columns = ['Terminal', 'TWS', 'ap', 'plan', 'fact', 'num_stop'])
            arrive1 = arrive1.append(arrive_temp, ignore_index = True)

        arr_f = arrive1
        stop_vs2 = ['09', '10A', '10B']
        arrChurk = ['ТАШКЕНТ', 'ДУШАНБЕ', 'ОШ', 'ХУДЖАНТ'] # добавлены черные рейсы
        arrB = arrive1[(arrive1.Terminal == 'B') & (arrive1.fact >= datetime.now() - timedelta(minutes = 40))]
        # увеличить задержку до 120 минут для черных рейсов
        arrB_churk = arrive1[(arrive1.Terminal == 'B') & (arrive1.ap.isin(arrChurk))
                             & (arrive1.fact >= datetime.now() - timedelta(minutes = 120))]
        arrA = arrive1[(arrive1.Terminal == 'A') & (arrive1.fact >= datetime.now() - timedelta(minutes = 20))]
        arrB3 = arrive1[(arrive1.num_stop.isin(stop_vs2)) & (arrive1.fact >= datetime.now() - timedelta(minutes = 40))]
        fltt.objects.update_or_create(pname = 'prilet_b', defaults = {'pznach': not arrB.empty or not arrB_churk.empty})
        fltt.objects.update_or_create(pname = 'prilet_a', defaults = {'pznach': not arrA.empty})
        fltt.objects.update_or_create(pname = 'prilet_b2', defaults = {'pznach': not arrB3.empty})
        time_now = datetime.now()
        tree_depart = etree.fromstring(depart)
        dep_f = DataFrame(columns = ['Terminal', 'TWS', 'plan', 'fact', 'num_stop', 'pos_beg', 'pos_end', 'reg_beg', 'reg_end'])
        for i in tree_depart:
            #     dateDepart = i.get('sdt')
            dateDepart = i.get('sort_1')
            time_plan = i.get('dt_plan')
            time_fact = i.get('dt_fact')
            pos_beg = i.get('pos_beg')
            pos_end = i.get('pos_end')
            reg_beg = i.get('reg_beg')
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
                reg_beg = datetime.strptime(dateDepart + ' ' + reg_beg, '%d-%b-%y %H:%M')
                if reg_beg > time_plan and time_plan != None:
                    reg_beg -= timedelta(days = 1)
            except ValueError:
                reg_beg = None
            try:
                reg_end = datetime.strptime(dateDepart + ' ' + reg_end, '%d-%b-%y %H:%M')
                if reg_end > time_plan and time_plan != None:
                    reg_end -= timedelta(days = 1)
            except ValueError:
                reg_end = None
            dep_f2 = DataFrame([[term, tws, time_plan, time_fact, num_stop, pos_beg, pos_end, reg_beg, reg_end]],
                               columns = ['Terminal', 'TWS', 'plan', 'fact', 'num_stop', 'pos_beg', 'pos_end', 'reg_beg',
                                          'reg_end'])
            dep_f = dep_f.append(dep_f2, ignore_index = True)

        stop_vs = ['07', '08', '09', '10A', '10B', '11', '12', '13', '14', '15']
        delta_minus = timedelta(minutes = 20)
        delta_plus = timedelta(minutes = 4)
        # delta_arr_minus = timedelta(minutes = 5)  # 5
        # delta_arr_plus = timedelta(minutes = 15)
        delta_dep_plan = timedelta(minutes = 45)
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
        # bFltt = fltt.objects.all()
        for s in stop_vs:
            znach = not arr1[(arr1.num_stop == s)].empty or not dep1[(dep1.num_stop == s)].empty
            fltt.objects.update_or_create(pname = 'park_' + s, defaults = {'pznach': znach})

        nakA = not dep_f[(dep_f.fact.isnull()) & (dep_f.reg_beg < time_now) & (dep_f.Terminal == 'A')].empty
        nakB = not dep_f[(dep_f.fact.isnull()) & (dep_f.reg_beg < time_now) & (dep_f.Terminal == 'B')].empty
        regA = not dep_f[(dep_f.fact.isnull()) & (dep_f.reg_beg < time_now) & (dep_f.reg_end > time_now) & (
        dep_f.Terminal == 'A')].empty
        regB = not dep_f[(dep_f.fact.isnull()) & (dep_f.reg_beg < time_now) & (dep_f.reg_end > time_now) & (
        dep_f.Terminal == 'B')].empty
        fltt.objects.update_or_create(pname = 'nakopitel_A', defaults = {'pznach': nakA})
        fltt.objects.update_or_create(pname = 'nakopitel_B', defaults = {'pznach': nakB})
        fltt.objects.update_or_create(pname = 'registr_A', defaults = {'pznach': regA})
        fltt.objects.update_or_create(pname = 'registr_B', defaults = {'pznach': regB})
