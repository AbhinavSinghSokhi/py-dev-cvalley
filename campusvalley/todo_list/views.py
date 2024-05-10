from django.shortcuts import render, redirect, HttpResponse
from .models import User, Task
from django.http import JsonResponse

from datetime import date
from django.contrib.auth import authenticate, login, logout
import json
import random, string

# Create your views here.
def index(request):
    return render(request, "index.html")

def signup(request):
    # password= request.session.get("password"), { 'password':password}
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


def get_data(request, num):
    all_tasks= [Task.objects.filter(user=request.user, completionStatus= False, dueDate= date.today()),
                Task.objects.filter(user=request.user, completionStatus= False, dueDate__gt= date.today()).order_by('dueDate'),
                Task.objects.filter(user=request.user, completionStatus= True),
                Task.objects.filter(user=request.user, completionStatus= False, category="personal"),
                Task.objects.filter(user=request.user, completionStatus= False, category="home"),
                Task.objects.filter(user=request.user, completionStatus= False, category="work")
                ]
    # print("inside get coubt fnction")
    return all_tasks[num]

def dashboard(request):
    # applying two filter here only rather than deleting the task from the database, task will stay saved only it's status will be changed on clicking check box and then it will redirect to the dahbaord where i only want to display those value whose completionStatus is False.
    today_user_tasks= get_data(request, 0)
    # Task.objects.filter(user=request.user, completionStatus= False, dueDate= date.today())
    upcoming_user_tasks= get_data(request, 1)
    # Task.objects.filter(user=request.user, completionStatus= False, dueDate__gt= date.today())
    completed_user_tasks=get_data(request, 2)
    # Task.objects.filter(user=request.user, completionStatus= True)
    personal_user_tasks= get_data(request,3)
    # Task.objects.filter(user=request.user, completionStatus= False, category="personal")
    home_user_tasks= get_data(request,4)
    # Task.objects.filter(user=request.user, completionStatus= False, category="home")
    work_user_tasks= get_data(request,5)
    # Task.objects.filter(user=request.user, completionStatus= False, category="work")
    # make dictionary or array of all these ,and access them seperately in all functions to make code simple and organized and reusbale

    return render(request, "dashboard.html", {'user_details': request.user ,"tasks": today_user_tasks, "num_of_tasks": len(today_user_tasks),
                                              'upcoming_tasks_count': len(upcoming_user_tasks),'completed_tasks_count':len(completed_user_tasks),
                                               'personal_tasks_count':len(personal_user_tasks), 'home_tasks_count':len(home_user_tasks),
                                                'work_tasks_count': len(work_user_tasks) })


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

        referring_url= request.META.get("HTTP_REFERER")
        print(referring_url)
        return redirect(referring_url)

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


def upcoming_tasks(request):
    today_user_tasks= get_data(request, 0)
    upcoming_user_tasks= get_data(request, 1)
    completed_user_tasks=get_data(request, 2)
    personal_user_tasks= get_data(request,3)
    home_user_tasks= get_data(request,4)
    work_user_tasks= get_data(request,5)
    return render(request, "upcoming_tasks.html",{'user_details': request.user ,"tasks": upcoming_user_tasks, "num_of_tasks": len(today_user_tasks),
                                              'upcoming_tasks_count': len(upcoming_user_tasks),'completed_tasks_count':len(completed_user_tasks),
                                               'personal_tasks_count':len(personal_user_tasks), 'home_tasks_count':len(home_user_tasks),
                                                'work_tasks_count': len(work_user_tasks)})

def completed_tasks(request):
    today_user_tasks= get_data(request, 0)
    upcoming_user_tasks= get_data(request, 1)
    completed_user_tasks=get_data(request, 2)
    personal_user_tasks= get_data(request,3)
    home_user_tasks= get_data(request,4)
    work_user_tasks= get_data(request,5)
    return render(request, "completed_tasks.html",{'user_details': request.user ,"tasks": completed_user_tasks,"num_of_tasks": len(today_user_tasks),
                                              'upcoming_tasks_count': len(upcoming_user_tasks),'completed_tasks_count':len(completed_user_tasks),
                                               'personal_tasks_count':len(personal_user_tasks), 'home_tasks_count':len(home_user_tasks),
                                                'work_tasks_count': len(work_user_tasks)} )

def personal_tasks(request):
    today_user_tasks= get_data(request, 0)
    upcoming_user_tasks= get_data(request, 1)
    completed_user_tasks=get_data(request, 2)
    personal_user_tasks= get_data(request,3)
    home_user_tasks= get_data(request,4)
    work_user_tasks= get_data(request,5)
    return render(request, "personal_tasks.html", {'user_details': request.user ,"tasks": personal_user_tasks, "num_of_tasks": len(today_user_tasks),
                                              'upcoming_tasks_count': len(upcoming_user_tasks),'completed_tasks_count':len(completed_user_tasks),
                                               'personal_tasks_count':len(personal_user_tasks), 'home_tasks_count':len(home_user_tasks),
                                                'work_tasks_count': len(work_user_tasks)})

def home_tasks(request):
    today_user_tasks= get_data(request, 0)
    upcoming_user_tasks= get_data(request, 1)
    completed_user_tasks=get_data(request, 2)
    personal_user_tasks= get_data(request,3)
    home_user_tasks= get_data(request,4)
    work_user_tasks= get_data(request,5)

    return render(request, "home_tasks.html", {'user_details': request.user ,"tasks": home_user_tasks, "num_of_tasks": len(today_user_tasks),
                                              'upcoming_tasks_count': len(upcoming_user_tasks),'completed_tasks_count':len(completed_user_tasks),
                                               'personal_tasks_count':len(personal_user_tasks), 'home_tasks_count':len(home_user_tasks),
                                                'work_tasks_count': len(work_user_tasks)})

def work_tasks(request):
    today_user_tasks= get_data(request, 0)
    upcoming_user_tasks= get_data(request, 1)
    completed_user_tasks=get_data(request, 2)
    personal_user_tasks= get_data(request,3)
    home_user_tasks= get_data(request,4)
    work_user_tasks= get_data(request,5)

    return render(request, "work_tasks.html", {'user_details': request.user ,"tasks": work_user_tasks, "num_of_tasks": len(today_user_tasks),
                                              'upcoming_tasks_count': len(upcoming_user_tasks),'completed_tasks_count':len(completed_user_tasks),
                                               'personal_tasks_count':len(personal_user_tasks), 'home_tasks_count':len(home_user_tasks),
                                                'work_tasks_count': len(work_user_tasks)})



def passwordgeneration (request):
    if request.method == "POST":
        pass_length= 10

        password_char= string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(password_char) for _ in range(pass_length))

        print(password)
    # request.session['password']= password
        return JsonResponse({'password':password})
    # return redirect (signup)