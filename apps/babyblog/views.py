from django.shortcuts import render, redirect
from django.contrib import messages
from models import User, Tweet

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

def tweet(request):
    if not session_check(request):
        return redirect('index')

    result = Tweet.objects.post_tweet(request)

    if result:
        print_errors(request, result)

    return redirect('babytwitter')

def destroy(request, id):
    if not session_check(request):
        return redirect('index')
    else:
        Tweet.objects.destroy_tweet(request, id)

        return redirect('babytwitter')

def babytwitter(request):
    if not session_check(request):
        return redirect('index')

    context = {
        'tweets': Tweet.objects.all()[::-1]
    }

    return render(request, 'babyblog/babytwitter.html', context)

def logout(request):
    request.session.clear()

    return redirect('index')
