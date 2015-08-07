from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import s_fault, CustomUser, s_commit, s_drop_lift
from .forms import s_faultForm, s_drop_liftForm, s_commitForm
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.mail import send_mail
# from django.contrib.flatpages.models import FlatPage
from django.template import Context, loader 
from datetime import datetime

@login_required
def list_otchet(request):
    args = {}
    # args.update(csrf(request))
    args['faults'] = s_fault.objects.select_related()
    args['username'] = request.user.last_name+' '+request.user.first_name
    return render_to_response('otchet.html', args)

# TODO: Сделать нормально, без редиректа.
@login_required
def profile(request):
    return redirect('/newpost/')

@login_required
def index(request):
    return render_to_response('index.html',)

def logout(request):
    auth.logout(request)
    return redirect('/accounts/login/')

@login_required
def newpost(request, postid):
    com = s_commit.objects.order_by('-id')[0]
    args = {}
    args.update(csrf(request))
    postid = int(postid)
    if postid:
        relative = get_object_or_404(s_fault, pk=postid)
        b = s_fault.objects.values().get(pk=postid)
        args['form'] = s_faultForm(b)
        # internation = s_fault.objects.select_related().get(pk=postid)
        # args['form'] = s_faultForm(initial={
            # 'fault_time': relative.fault_time,
            # 'f_system': relative.f_system,
            # 's_object': relative.s_object,
            # 'description': relative.description,
            # 'correction': relative.correction,})
        args['buttonName'] = 'Записать'
    else:
        args['form'] = s_faultForm
        args['buttonName'] = 'Добавить'
    args['faults'] = s_fault.objects.select_related().filter(pk__gt=com.s_fault_commit_id)
    args['lift_form'] = s_drop_liftForm
    args['lifts'] = s_drop_lift.objects.select_related().filter(pk__gt=com.s_lift_commit_id)
    args['commit_form'] = s_commitForm
    args['username'] = request.user.last_name+' '+request.user.first_name
    args['postid'] = postid
    return render_to_response('newpost.html', args)

@login_required
def addpost(request):
    if request.POST:
        form = s_faultForm(request.POST)
        if form.is_valid:
            npost = form.save(commit=False)
            npost.f_staff = CustomUser.objects.get(username=request.user.username)
            # postid = int(request.POST.postid)
            # if postid:
            #     npost.pk=postid
            form.save()
    return redirect('/newpost/0/')

@login_required
def addliftfault(request):
    if request.POST:
        form = s_drop_liftForm(request.POST)
        if form.is_valid:
            nlift = form.save()
    return redirect('/newpost/')

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
        'Django test mail',
        '<p>This is an <strong>important</strong> message.</p>',
        'tich31337@yandex.ru',
        ['tich31337@gmail.com',],
        html_message=body_html,)
    commit = s_commit(
        s_time= datetime.now(),
        s_fault_commit = s_fault.objects.order_by('-id')[0],
        s_lift_commit = s_drop_lift.objects.order_by('-id')[0],
        s_prim = args['prim'],
        s_staff_commit = CustomUser.objects.get(username=request.user.username),)
    commit.save()
    return redirect('/newpost/')