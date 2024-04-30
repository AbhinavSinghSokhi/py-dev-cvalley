from django.shortcuts import render, redirect, HttpResponse
from .models import User, Task
from django.contrib.auth import authenticate, login, logout
import json
# Create your views here.
def index(request):
    return render(request, "index.html")

def signup(request):
    return render(request, "signup.html")

def loginForm(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(dashboard)
        else:
            return render(request, 'index.html', {'error': 'Invalid Credentials'})
    else:
        return render(request, "index.html")


def signupForm(request):
    if request.method=="POST":
        username= request.POST.get("username")
        email= request.POST.get("email")
        password= request.POST.get("password")
        User.objects.create_user(username=username, email=email, password=password)
        return redirect(index)
    else:
        return render(request, "signup.html")

def dashboard(request):
    # applying two filter here only rather than deleting the task from the database, task will stay saved only it's status will be changed on clicking check box and then it will redirect to the dahbaord where i only want to display those value whose completionStatus is False.
    user_tasks= Task.objects.filter(user=request.user, completionStatus= False)

    # print(user_tasks)
    return render(request, "dashboard.html", {'user_details': request.user ,"tasks": user_tasks})


def new_task(request):
    if request.method=="POST":
        task_title= request.POST.get("task_title")
        task_desc= request.POST.get("task_desc")
        task_category= request.POST.get("list")
        task_due_date= request.POST.get("due_date")
        # response= task_title + " " + task_desc+ " " + task_category + " "+ task_due_date
        # return HttpResponse(response, status=200)
        user= request.user
        user_name= User.objects.get(username= user.username)
        task= Task.objects.create(user= user_name, title=task_title, description=task_desc, category=task_category, dueDate=task_due_date )
        # return render(request, "dashboard.html",{'user_details': request.user} )
        return redirect(dashboard)
    else:
        return redirect(dashboard)

def delete_task(request):
    if request.method=="POST":
        taskId= request.POST.get("task_id")
        # print(taskId)
        object_to_del= Task.objects.get(task_id=taskId)
        object_to_del.delete()
        return redirect(dashboard)

def mark_completed (request):
    if request.method=="POST":
        data= json.loads(request.body)
        taskId= data.get('task_id')
        isCompleted =  data.get('is_completed')
        # print("task_id: ",taskId, isCompleted)
        statusChange = Task.objects.get(task_id= taskId)
        statusChange.completionStatus= isCompleted
        statusChange.save()
        return redirect(dashboard)
    else:
        return  redirect(dashboard)

def logout_user(request):
    logout(request)
    return redirect(index)