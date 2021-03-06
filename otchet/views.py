from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .models import s_fault, s_commit, s_drop_lift, s_system, s_fault_lift
from .forms import s_faultForm, s_drop_liftForm, s_commitForm
from django.contrib import auth
from django.template.context_processors import csrf
from django.core.mail import send_mail
from django.template import Context, loader
from datetime import datetime, timedelta, date
from collections import OrderedDict
from django.template import RequestContext



# from django.utils import json

@login_required
def list_otchet(request, start_time = date.today() - timedelta(days = 1),
                stop_time = date.today() + timedelta(days = 1)):
    args = {}
    # args.update(csrf(request))
    # faults = s_fault.objects.select_related()
    # lifts = s_drop_lift.objects.select_related()
    if request.GET:
        if request.GET.get('start_time'):
            start_time = datetime.strptime(request.GET.get('start_time'), '%Y-%m-%dT%H:%M')
        if request.GET.get('stop_time'):
            stop_time = datetime.strptime(request.GET.get('stop_time'), '%Y-%m-%dT%H:%M')
    args['start_time'] = start_time.strftime('%Y-%m-%dT%H:%M')
    args['stop_time'] = stop_time.strftime('%Y-%m-%dT%H:%M')
    args['faults'] = s_fault.objects.filter(fault_time__gte = start_time, fault_time__lte = stop_time)
    args['lifts'] = s_drop_lift.objects.filter(stop_lift__gte = start_time, stop_lift__lte = stop_time)
    # faults = faults.filter(fault_time__lte=stop_time)
    # lifts = lifts.filter(stop_lift__lte=stop_time)
    # args['faults'] = faults
    # args['lifts'] = lifts
    # args['username'] = request.user.get_full_name()
    return render_to_response('otchet.html', args, context_instance=RequestContext(request))

@login_required
def otchet_td(request, start_time = date.today() - timedelta(days = 10 + datetime.weekday(date.today())),
                stop_time = date.today() - timedelta(days = 3 + datetime.weekday(date.today()))):
    args = {}
    if request.GET:
        if request.GET.get('start_time'):
            start_time = datetime.strptime(request.GET.get('start_time'), '%Y-%m-%dT%H:%M')
        if request.GET.get('stop_time'):
            stop_time = datetime.strptime(request.GET.get('stop_time'), '%Y-%m-%dT%H:%M')
    args['start_time'] = start_time.strftime('%Y-%m-%dT%H:%M')
    args['stop_time'] = stop_time.strftime('%Y-%m-%dT%H:%M')
    args['fire'] = s_fault.objects.filter(fault_time__gte = start_time, fault_time__lte = stop_time, f_system = 1,)
    args['lifts'] = s_drop_lift.objects.filter(stop_lift__gte = start_time, stop_lift__lte = stop_time, fault_id = 1,)
    args['username'] = request.user.get_full_name()
    fault_sys = s_system.objects.all()
    lift = s_fault_lift.objects.all()
    fault_count ={}
    lift_count ={}
    for fau in fault_sys:
        fault_count[fau.system_name] = s_fault.objects.filter(f_system__system_name = fau.system_name,
                                                              fault_time__gte = start_time,
                                                              fault_time__lte = stop_time, ).count()
    for l in lift:
        lift_count[l.type_fault] = s_drop_lift.objects.filter(fault__type_fault = l.type_fault,
                                                              stop_lift__gte = start_time,
                                                              stop_lift__lte = stop_time, ).count()
    # print(fault_count)
    # args['f_count'] = list(fault_count.keys()).sort()
    # args['l_count'] = list(lift_count.keys()).sort()
    args['fault_count'] = OrderedDict(sorted(fault_count.items(), key=lambda t: t[0]))
    args['lift_count'] = OrderedDict(sorted(lift_count.items(), key=lambda t: t[0]))
    return render_to_response('otchet_td.html', args, context_instance=RequestContext(request))


# TODO: Сделать нормально, без редиректа.
@login_required
def profile(request):
    return redirect('/')


@login_required
def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    return redirect('/accounts/login/')


@login_required
def newpost(request, postid = 0, liftid = 0):
    postid = int(postid)
    liftid = int(liftid)
    try:
        # com = s_commit.objects.order_by('-id')[0]  # получаем последний закоммиченный объект
        com = s_commit.objects.last()  # получаем последний закоммиченный объект
    except s_commit.DoesNotExist:
        postid = False
        liftid = False
    args = {}
    args.update(csrf(request))
    # if request.GET:
    #     postid = int(request.GET['data'])
    if postid:
        relative = get_object_or_404(s_fault, pk = postid)
        if postid > com.s_fault_commit_id:
            # b = s_fault.objects.filter(pk=postid).select_related()
            # for a in b:
            # args['form'] = s_faultForm(initial=a)
            args['form'] = s_faultForm(initial = {
                # 'fault_time': (relative.fault_time+timedelta(hours=5)).strftime('%d.%m.%Y %H:%M'),
                'fault_time': (relative.fault_time + timedelta(hours = 5)).strftime('%Y-%m-%dT%H:%M'),
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
    if liftid:
        liftbd = get_object_or_404(s_drop_lift, pk = liftid)
        if liftid > com.s_lift_commit_id:
            args['lift_form'] = s_drop_liftForm(initial = {
                'stop_lift': (liftbd.stop_lift + timedelta(hours = 5)).strftime('%Y-%m-%dT%H:%M'),
                'start_lift': (liftbd.start_lift + timedelta(hours = 5)).strftime('%Y-%m-%dT%H:%M'),
                'lift_name': liftbd.lift_name,
                'fault': liftbd.fault,
                'description': liftbd.description,
                'consequences': liftbd.consequences,
            })
            args['button_lift_name'] = 'Записать'
            args['liftid'] = liftid
    else:
        args['lift_form'] = s_drop_liftForm
        args['button_lift_name'] = 'Добавить'
        args['liftid'] = 0
    try:
        args['faults'] = s_fault.objects.select_related().filter(pk__gt = com.s_fault_commit_id)
        args['lifts'] = s_drop_lift.objects.select_related().filter(pk__gt = com.s_lift_commit_id)
    except:
        pass
    args['commit_form'] = s_commitForm
    args['username'] = request.user.get_full_name()
    return render_to_response('newpost.html', args, context_instance=RequestContext(request))


@login_required
def addpost(request):
    if request.POST:
        cPost = request.POST.copy()
        cPost['fault_time'] = datetime.strptime(cPost['fault_time'], '%Y-%m-%dT%H:%M')
        form = s_faultForm(cPost)
        if form.is_valid():
            # try:
            npost = form.save(commit = False)
            npost.f_staff = CustomUser.objects.get(username = request.user.username)
            postid = int(request.POST.get('postid'))
            if postid:
                npost.pk = postid
            form.save()
    return redirect('/')
    # TODO: сделать через AJAX
    # return render_to_response('newpost.html', locals())


@login_required
def delpost(request, postid):
    com = s_commit.objects.order_by('-id')[0]  # получаем последний закоммиченный объект
    postid = int(postid)
    if postid > com.s_fault_commit_id:
        try:
            s_fault.objects.get(pk = postid).delete()
        except:
            pass

    # return redirect('/')
    return HttpResponse('Ok')

@login_required
def addliftfault(request):
    if request.POST:
        test = request.POST.copy()
        test['stop_lift'] = datetime.strptime(test['stop_lift'], '%Y-%m-%dT%H:%M')
        test['start_lift'] = datetime.strptime(test['start_lift'], '%Y-%m-%dT%H:%M')
        form = s_drop_liftForm(test)
        if form.is_valid():
            nlift = form.save(commit = False)
            liftid = int(request.POST.get('liftid'))
            if liftid:
                nlift.pk = liftid
            form.save()
    return redirect('/')
    # TODO: сделать без редиректа, через AJAX
    # return HttpResponse('Ok')

@login_required
def newmail(request):
    # mail_template = '/otchet.html'
    com = s_commit.objects.order_by('-id')[0]
    t = loader.get_template('sendotchet.html')
    args = {}
    args['faults'] = s_fault.objects.select_related().filter(pk__gt = com.s_fault_commit_id)
    args['lifts'] = s_drop_lift.objects.select_related().filter(pk__gt = com.s_lift_commit_id)
    args['username'] = request.user.get_full_name()
    args['d_otch'] = datetime.now()
    args['prim'] = ''
    if request.POST:
        form = s_commitForm(request.POST)
        if form.is_valid() and request.POST['s_prim']:
            args['prim'] = request.POST['s_prim']
    body_html = t.render(Context(args))
    send_mail(
        'Сдача смены ' + str(date.today()) + ' ' + args['username'],
        args['username'],
        '5704@koltsovo.ru',
        ['tich31337@gmail.com', ],
        html_message = body_html, )
    commit = s_commit(
        s_time = datetime.now(),
        s_fault_commit = s_fault.objects.order_by('-id')[0],
        s_lift_commit = s_drop_lift.objects.order_by('-id')[0],
        s_prim = args['prim'],
        s_staff_commit = CustomUser.objects.get(username = request.user.username),
        )
    commit.save()
    return redirect('/accounts/logout/')
    # return HttpResponse('Ok')

@login_required
def fault_correct(request):
    # context = {}
    try:
        com = s_commit.objects.order_by('-id')[0]
        postid = int(request.GET['data'])
        if postid > com.s_fault_commit_id:
            postdb = s_fault.objects.get(pk = postid)
            postdb.correction = not postdb.correction
            postdb.save()
    except:
        pass
        # context['text'] = 'error'
        # else:
        # context['text'] = data[::-1]
    # return redirect('/')
    return HttpResponse('Ok')

@login_required
def lift_del(request):
    # try:
    com = s_commit.objects.order_by('-id')[0]
    postid = int(request.GET['data'])
    if postid > com.s_lift_commit_id:
        s_drop_lift.objects.get(pk = postid).delete()
        # except:
        # pass
    # return redirect('/')
    return HttpResponse('Ok')