from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from pymongo.mongo_client import MongoClient

client = MongoClient(
    "mongodb+srv://projectManagementPortal:projectManagementPortal@cluster0.abehjnm.mongodb.net?retryWrites=true&w=majority")
db = client.get_database('ProjectManagementDB')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        print(username, pass1)

    collections = db['users']

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        # user = authenticate(request, username=username, password=pass1)
        print(username, pass1)
        if username == 'admin' and pass1 == 'admin':
            request.session['username'] = username
            return redirect('/admin')

        redirect_url = request.session.get('redirectTo')

        if redirect_url is None:
            redirect_url = "/home"

        reply = collections.find_one({"username": username})

        print("redirect_url is ", redirect_url)
        if reply is not None:
            # print("reply is not nones")
            if reply["password"] == pass1:
                print("Login Successful")
                request.session['username'] = username
                if redirect_url is not None:
                    print("username saved is ", request.session.get('username'))
                    request.session['redirectTo'] = None
                    return redirect(redirect_url)
                return redirect('/home')
            else:
                print("Password is incorrect")
                print("redirect_url is ", request.session.get('redirectTo'))
                template = loader.get_template("login.html")
                context = {
                    "fail": True,
                    "redirect_url": redirect_url,
                }
                return render(request, 'login.html', context)
        else:
            template = loader.get_template("login.html")
            context = {
                "fail": True,
                "redirect_url": redirect_url,
            }
            return HttpResponse(template.render(context, request))

    return render(request, 'login.html')


def register(request):
    return render(request, 'signup.html')


def home(request):
    return render(request, 'home.html')


def logout(request):
    request.session['username'] = None
    return redirect('/home')


def forget_password(request):
    return "<h1>Dummy</h1>"


def dashboard(request):
    username = request.session.get('username')

    context = {
        "username": username,
    }
    return render(request, 'dashboard.html', context)
