from django.shortcuts import render, redirect
from django.contrib import messages
from models import User, Message

def session_check(request):
    if 'user' in request.session:
        return True
    else:
        return False

def index(request):
    if session_check(request):
        return redirect('babytwitter')
    else:
        return render(request,'babyblog/index.html')

def login_reg(request):
    if request.POST['action'] == 'register':
        result = User.objects.validate_reg(request)

    elif request.POST['action'] == 'login':
        result = User.objects.validate_login(request)

    if result[0] == False:
        print_errors(request, result[1])
        return redirect('/')

    return log_user_in(request, result[1])

def print_errors(request, error_list):
    for error in error_list:
        messages.add_message(request, messages.INFO, error)

def log_user_in(request, user):
    request.session['user'] = {
        'user_id': user.id,
        'user_name': user.user_name
    }

    return redirect('babytwitter')

def message(request):
    if not session_check(request):
        return redirect('index')

    result = Message.objects.post_message(request)

    if result:
        print_errors(request, result)

    return redirect('babytwitter')

def destroy(request, id):
    if not session_check(request):
        return redirect('index')
    else:
        Message.objects.destroy_message(request, id)

        return redirect('wall')

def babytwitter(request):
    if not session_check(request):
        return redirect('index')

    context = {
        'messages': Message.objects.all()[::-1]
    }

    return render(request, 'babytwitter.html', context)

def logout(request):
    request.session.clear()

    return redirect('index')
