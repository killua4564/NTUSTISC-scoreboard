from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .models import *


def is_login(request):
    if 'username' in request.session.keys():
        if len(request.session['username']) > 0:
            return True
        else:
            return False
    else:
        return False


def index(request):
    challenge_list = Challenge.objects.all()
    submit_list = Submit.objects.all().order_by('-id')[:20]
    logined = is_login(request)
    if logined:
        challenge_list = []
        username = Username.objects.get(username=request.session['username'])
        for challenge in Challenge.objects.all():
            challenge.user_solve = Submit.objects.filter(
                username=username,
                challenge=challenge
            ).exists()
            challenge_list.append(challenge)
    return render(request, "index.html", {
        'key': logined,
        'username': request.session['username'] if logined else None,
        'challenge_list': challenge_list,
        'submit_list': submit_list
    })


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if Username.objects.filter(username=username).exists():
            user = Username.objects.get(username=username)
        else:
            user = Username.objects.create(username=username)
        request.session['username'] = user.username
    return redirect("../")


def flag(request):
    if request.method == 'POST':
        flag = request.POST.get('flag').strip()
        if Challenge.objects.filter(flag=flag).exists():
            username = Username.objects.get(
                username=request.session['username'])
            challenge = Challenge.objects.get(flag=flag)
            if not Submit.objects.filter(username=username, challenge=challenge).exists():
                Submit.objects.create(username=username, challenge=challenge)
                username.solved += 1
                username.save()
                challenge.solved += 1
                challenge.save()
                return JsonResponse({
                    'correct': True,
                    'message': "Flag 正確！"
                })
            else:
                return JsonResponse({
                    'correct': True,
                    'message': "Flag 是正確沒錯，但你已經解過這題了"
                })
        else:
            return JsonResponse({
                'correct': False,
                'message': "Flag 錯誤 QQ"
            })
    else:
        return HttpResponse("<h1>OAO?</h1>")
