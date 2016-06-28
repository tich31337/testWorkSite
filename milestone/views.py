# -*- coding: utf-8 -*-
__author__ = 'tich'

from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from .serializers import CameraSerializer

# Необходимый параметр в settings
# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.core.context_processors.auth'
# )

from .models import MilestoneUser, MilLogin, sysSec, MilCamera, MilLogin2

from datetime import datetime, timedelta
import requests


# тестирование сервера. На продакшене изменить
@login_required()
def milestoneOtchet(request):
    args = {}
    resp = requests.post('http://192.168.0.140:5000/users')
    a = resp.json()
    b = a.pop('list')
    args['list'] = sorted(b, key = lambda d: (d['lUser'].lower(), d['lQuant']))
    # args['username'] = request.user.last_name + ' ' + request.user.first_name
    return render_to_response('otchet_ip.html', args, context_instance=RequestContext(request))

# @login_required()
@permission_required('milestone.can_read_ml')
@csrf_protect
def milestoneBD(request, bdSort=False):
    args = {}
    listUser = []
    # args['username'] = request.user.get_full_name()
    setBd = set()
    setDate = set()
    listBd = MilLogin.objects.filter(lDate__gte = datetime.now()-timedelta(7)).order_by('lUser', 'lDate')
    listUsM =  sysSec.objects.all()
    for lb in listBd:
        setBd.add(str(lb.lUser) +' '+ str(lb.lIP))

    for sb in setBd:
        sbUser, sbIP = sb.split()
        validIP = False
        for lum in listUsM:
            if (sbUser == str(lum.milUser) and sbIP == str(lum.ipAddress)) or (sbIP == str(lum.ipAddress) and lum.miAdmin):
                validIP = True
        dataCount = [0]*7
        for lb in listBd:
            i = 0
            for td in range(7,0,-1):
                sd = datetime.strftime(datetime.today()-timedelta(td), '%Y-%m-%d')
                setDate.add(sd)
                if (sbUser in str(lb)) and (sbIP in str(lb)) and (sd in str(lb)):
                    dataCount[i] = lb.lQuant
                i += 1
        listUser.append({'lUser':sbUser, 'lIP':sbIP, 'dataCount': dataCount, 'validIP': validIP})
    if bdSort:
        args['list'] = sorted(listUser, key = lambda d: (d['lUser'].lower(), d['lIP']))
    else:
        args['list'] = sorted(listUser, key = lambda d: (d['validIP'], d['lUser'].lower(), d['lIP']))
    args['setDate'] = sorted(setDate)
    return render_to_response('otchet_ip.html', args, context_instance=RequestContext(request))

# TODO: Сделать отправку email при входе невалидированных пользователей

@login_required()
def milestoneValid(request):
    try:
        userIP = str(request.POST['dtIP'])
        userUser = str(request.POST['dtUser'])
        sysBD = sysSec.objects.get(ipAddress = userIP)
        userBD = MilestoneUser.objects.get(loginName = userUser)
        if sysBD.milUser == userBD:
            sysBD.milUser = None
        else:
            sysBD.milUser = userBD
        sysBD.save()
    except:
        return HttpResponse('err')
    return HttpResponse('Ok')
    # return redirect('/otchetbd/')

@api_view(['POST',])
def createCamera(request):
    if request.method == 'POST':
        try:
            for d in request.data:
                serializer = CameraSerializer(data = d)
                print(serializer)
                if serializer.is_valid():
                    serializer.update()
                    print("ok")
                else:
                    print('false', serializer.errors)
            return Response(status = status.HTTP_201_CREATED)
        except:
            return Response(status = status.HTTP_400_BAD_REQUEST)
    if not request.data:
        return Response(status = status.HTTP_204_NO_CONTENT)
    return Response('bad',status = status.HTTP_404_NOT_FOUND)

class updateCamera(mixins.UpdateModelMixin):

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
