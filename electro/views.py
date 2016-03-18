from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
import pandas as pd
import pypyodbc as pyodbc
import pymssql
from datetime import datetime, timedelta


from .models import energosfera,nameCount

# @permission_required('electro.can_read_electro')
# def electro1(request):
#     args = {}
#     el = energosfera.objects.filter(eDate__gte = datetime.now()-timedelta(days = 5))
#     df = pd.DataFrame({'eId' : [str(e.eId) for e in el],'eDate':[e.eDate for e in el], 'ekWt':[e.ekwt for e in el]})
#     el = df.groupby(['eId','eDate']).mean().unstack().to_csv()
#     el = el.split('\n')
#     # el[0] = 'Дата'
#     a = []
#
#     strDate = el[1].split(',')
#     strDate[0] = 'Дата'
#     d =[]
#     for i in strDate[1:]:
#         d.append(datetime.strptime(i,'%Y-%m-%d %H:%M:%S.%z'))
#     args['strDate'] = d
#     el = el[3:]
#     for i in el:
#         a.append(i.split(','))
#         # print(i)
#     args['el'] = a
#     # print(args['el'])
#     return render_to_response('electro.html',args, context_instance=RequestContext(request))

@permission_required('electro.can_read_electro')
def electro2(request):
    args = {}
    dsn = 'energosource'
    # dsn = 'sqlserver'
    user = 'SUDIO'
    password = 'Gnbks877N'
    database = 'sudio_perm'
    con_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, user, password, database)
    # energosfera = pyodbc.connect(con_string)
    energosfera = pymssql.connect(server='192.168.80.4', user=user, password=password, database=database)

    # energosfera = pyodbc.connect('DRIVER={FreeTDS};SERVER=192.168.80.4;DATABASE=sudio_perm;UID=SUDIO;PWD=Gnbks877N')
    # cursor = energosfera.cursor()
    d2 = datetime.today() - timedelta(7)
    nameCount = pd.read_csv("electro/name2.csv", error_bad_lines=False, sep=';')
    # d2 = date(2015, 12,3)
    qwery2 = "SELECT ID_PP, (CAST(M as varchar(2)) + '/' + CAST(D as varchar(2)) + '/' + CAST(Y as varchar(4))) AS date, "\
                +"(CAST(H as varchar(2))+':00') as time,  value FROM PP_hours WHERE Y >="\
                +d2.strftime('%Y')+" AND M >="+d2.strftime('%m')+" AND D >="+d2.strftime('%d')
    kt = pd.read_sql(qwery2, energosfera)
    kt.date = kt.date.apply(pd.to_datetime)
    kt = pd.merge(nameCount, kt, on='ID_PP')
    # print(d2)
    d3 = kt.pivot_table(['value'],['ind','Наименование','date'],aggfunc='sum')
    # d3 = d3.unstack('Наименование')
    d3 = d3.unstack('date')
    args['el'] = d3.round(2).to_html()
    # print(args['el'])

    return render_to_response('electro.html',args, context_instance=RequestContext(request))