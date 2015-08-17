from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import s_fault, CustomUser, s_commit, s_drop_lift
from .forms import s_faultForm, s_drop_liftForm, s_commitForm, SMForm
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.mail import send_mail
# from django.contrib.flatpages.models import FlatPage
from django.template import Context, loader 
from datetime import datetime, timedelta
# from django.utils import json

@login_required
def list_otchet(request):
    args = {}
    args.update(csrf(request))
    faults = s_fault.objects.select_related()
    lifts = s_drop_lift.objects.select_related()
    if request.POST:
        if request.POST.get('start_time'):
            start_time = datetime.strptime(request.POST.get('start_time'), '%Y-%m-%dT%H:%M')
            faults = faults.filter(fault_time__gte=start_time)
            lifts = lifts.filter(stop_lift__gte=start_time)
            args['start_time'] = request.POST.get('start_time')
        if request.POST.get('stop_time'):
            stop_time = datetime.strptime(request.POST.get('stop_time'), '%Y-%m-%dT%H:%M')
            faults = faults.filter(fault_time__lte=stop_time)
            lifts = lifts.filter(stop_lift__lte=stop_time)
            args['stop_time'] = request.POST.get('stop_time')
    args['faults'] = faults
    args['lifts'] = lifts
    args['username'] = request.user.last_name+' '+request.user.first_name
    return render_to_response('otchet.html', args)

# TODO: Сделать нормально, без редиректа.
@login_required
def profile(request):
    return redirect('/')

@login_required
def index(request):
    return render_to_response('index.html',)

def logout(request):
    auth.logout(request)
    return redirect('/accounts/login/')

@login_required
def newpost(request, postid=0, liftid=0):
    com = s_commit.objects.order_by('-id')[0] # получаем последний закоммиченный объект
    postid = int(postid)
    args = {}
    args.update(csrf(request))
    # if request.GET:
    #     postid = int(request.GET['data'])
    if postid:
        relative = get_object_or_404(s_fault, pk=postid)
        if postid > com.s_fault_commit_id:
        # b = s_fault.objects.filter(pk=postid).select_related()
        # for a in b:
            # args['form'] = s_faultForm(initial=a)
            args['form'] = s_faultForm(initial={
                'fault_time': (relative.fault_time+timedelta(hours=5)).strftime('%d.%m.%Y %H:%M'),
                'f_system': relative.f_system,
                's_object': relative.s_object,
                'description': relative.description,
                'correction': relative.correction,
                })
            args['buttonName'] = 'Записать'
            args['postid'] = postid
    else:
        args['form'] = s_faultForm
        args['buttonName'] = 'Добавить'
        args['postid'] = 0
    liftid = int(liftid)
    if liftid:
        liftbd = get_object_or_404(s_drop_lift, pk=liftid)
        if liftid > com.s_lift_commit_id:
            args['lift_form'] = s_drop_liftForm(initial={
                'stop_lift' : (liftbd.stop_lift+timedelta(hours=5)).strftime('%d.%m.%Y %H:%M'),
                'start_lift' : (liftbd.start_lift+timedelta(hours=5)).strftime('%d.%m.%Y %H:%M'),
                'lift_name': liftbd.lift_name,
                'fault' : liftbd.fault,
                'description' : liftbd.description,
                'consequences' : liftbd.consequences,
                })
            args['button_lift_name'] = 'Записать'
            args['liftid'] = liftid
    else:
        args['lift_form'] = s_drop_liftForm
        args['button_lift_name'] = 'Добавить'
        args['liftid'] = 0
    args['faults'] = s_fault.objects.select_related().filter(pk__gt=com.s_fault_commit_id)
    args['lifts'] = s_drop_lift.objects.select_related().filter(pk__gt=com.s_lift_commit_id)
    args['commit_form'] = s_commitForm
    args['username'] = request.user.last_name+' '+request.user.first_name
    return render_to_response('newpost.html', args)

@login_required
def addpost(request):
    if request.POST:
        form = s_faultForm(request.POST)
        if form.is_valid:
            npost = form.save(commit=False)
            npost.f_staff = CustomUser.objects.get(username=request.user.username)
            postid = int(request.POST.get('postid'))
            if postid:
                npost.pk=postid
            form.save()
    return redirect('/')

@login_required
def delpost(request, postid):
    com = s_commit.objects.order_by('-id')[0] # получаем последний закоммиченный объект
    postid = int(postid)
    if postid > com.s_fault_commit_id:
        try:
            s_fault.objects.get(pk=postid).delete()
        except:
            pass

    return redirect('/')

@login_required
def addliftfault(request):
    if request.POST:
        form = s_drop_liftForm(request.POST)
        if form.is_valid:
            nlift = form.save(commit=False)
            liftid = int(request.POST.get('liftid'))
            if liftid:
                nlift.pk=liftid
            form.save()
    return redirect('/')

@login_required
def newmail(request):
    # mail_template = '/otchet.html'
    com = s_commit.objects.order_by('-id')[0]
    t = loader.get_template('sendotchet.html')
    args = {}
    args['faults'] = s_fault.objects.select_related().filter(pk__gt=com.s_fault_commit_id)
    args['lifts'] = s_drop_lift.objects.select_related().filter(pk__gt=com.s_lift_commit_id)
    args['username'] = request.user.last_name+' '+request.user.first_name
    args['d_otch'] = datetime.now()
    args['prim'] = ''
    if request.POST:
        form = s_commitForm(request.POST)
        if form.is_valid and request.POST['s_prim']:
            args['prim'] = request.POST['s_prim']
    body_html = t.render(Context(args))
    send_mail(
        'Сдача смены',
        'Сменный инженер',
        '5704@koltsovo.ru',
        ['tich31337@gmail.com',],
        html_message=body_html,)
    commit = s_commit(
        s_time= datetime.now(),
        s_fault_commit = s_fault.objects.order_by('-id')[0],
        s_lift_commit = s_drop_lift.objects.order_by('-id')[0],
        s_prim = args['prim'],
        s_staff_commit = CustomUser.objects.get(username=request.user.username),)
    commit.save()
    return redirect('/')

@login_required
def fault_correct(request):
    # context = {}
    try:
        com = s_commit.objects.order_by('-id')[0]
        postid = int(request.GET['data'])
        if postid > com.s_fault_commit_id:
            postdb = s_fault.objects.get(pk=postid)
            postdb.correction = not postdb.correction
            postdb.save()
    except:
        pass
        # context['text'] = 'error'
    # else:
        # context['text'] = data[::-1]
    return redirect('/')

@login_required
def lift_del(request):
    # try:
    com = s_commit.objects.order_by('-id')[0]
    postid = int(request.GET['data'])
    if postid > com.s_lift_commit_id:
        s_drop_lift.objects.get(pk=postid).delete()
    # except:
        # pass
    return redirect('/')    