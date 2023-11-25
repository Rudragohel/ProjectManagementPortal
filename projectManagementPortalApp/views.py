from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from pymongo.mongo_client import MongoClient

client = MongoClient(
    "mongodb+srv://projectManagementPortal:projectManagementPortal@cluster0.abehjnm.mongodb.net?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.get_database('ProjectManagementDB')


def login(request):
    print(request.POST)
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('pass')
        print(username, password)

    collections = db['users']

    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('pass')
        # user = authenticate(request, username=username, password=pass1)
        print(email, pass1)

        redirect_url = request.session.get('redirectTo')

        if redirect_url is None:
            redirect_url = "/dashboard/"

        reply = collections.find_one({"email": email})
        print("reply is ", reply)
        print("redirect_url is ", redirect_url)
        if reply is not None:
            # print("reply is not nones")
            if reply["password"] == pass1:
                print("Login Successful")
                request.session['username'] = reply["firstname"]
                if redirect_url is not None:
                    print("username saved is ", request.session.get('username'))
                    request.session['redirectTo'] = None
                    return redirect(redirect_url)
                return redirect('/dashboard/')
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

    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        emailID = request.POST.get('emailID')
        studentID = request.POST.get('studentID')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        usertype = request.POST.get('userType')
        print(request.POST)
        collections = db['users']

        if username is None:
            username = "null"
        if studentID == "":
            studentID = "null"

        if password == repassword and collections.find_one({"email": emailID}) is None:
            collections.insert_one({
                "firstname": firstname,
                "lastname": lastname,
                "username": username,
                "email": emailID,
                "studentID": studentID,
                "password": password,
                "usertype": usertype,
            })
            return redirect('/dashboard')
        else:
            print("Password doesn't match or email already exists")
    return render(request, 'signup.html')


def home(request):
    return render(request, 'login.html')


def logout(request):
    request.session['username'] = None
    return redirect('/home')


def forget_password(request):
    return "<h1>Dummy</h1>"


def dashboard(request):
    print("dashboard called")
    username = request.session.get('username')
    print("username is ", username)

    if username is None:
        request.session['redirectTo'] = '/dashboard/'
        context = {
            "message": "Please login to continue",
            "type": "error",
            "display": True,
        }
        return render(request, 'login.html', context)

    context = {
        "display": False,
        "username": username,
    }
    return render(request, 'dashboard.html', context)
