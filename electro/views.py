from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from pandas import DataFrame, Series
import pandas as pd
from datetime import datetime, timedelta

from .models import energosfera,nameCount

@permission_required('electro.can_read_electro')
def electro1(request):
    args = {}
    el = energosfera.objects.filter(eDate__gte = datetime.now()-timedelta(days = 5))
    df = DataFrame({'eId' : [str(e.eId) for e in el],'eDate':[e.eDate for e in el], 'ekWt':[e.ekwt for e in el]})
    el = df.groupby(['eId','eDate']).mean().unstack().to_csv()
    el = el.split('\n')
    # el[0] = 'Дата'
    a = []

    strDate = el[1].split(',')
    strDate[0] = 'Дата'
    d =[]
    for i in strDate[1:]:
        d.append(datetime.strptime(i,'%Y-%m-%d %H:%M:%S.%z'))
    args['strDate'] = d
    el = el[3:]
    for i in el:
        a.append(i.split(','))
        # print(i)
    args['el'] = a
    # print(args['el'])
    return render_to_response('electro.html',args, context_instance=RequestContext(request))