from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


def test_view(request):
    return render(request, 'index.html', {})

def login_user(request):
    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )
    if user in None:
        return render_to_response('error.html', {})
    else:
        login(request, user)
        return HttpResponseRedirect('/')
