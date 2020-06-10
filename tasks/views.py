from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404
from tasks.models import Task
from tags.models import *
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User




# Create your views here.

def task_index(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')
    user = User.objects.get(id=request.user.id)
    tasks = user.tasks.all()

    #tasks = Task.objects.all()
    taskTagIntegration = TagsTaskIntegration.objects.all()
    tags = Tag.objects.all()
    return render(request, 'index.html', {'tasks': tasks, 'taskTagIntegration': taskTagIntegration, 'tags': tags})

@csrf_exempt
def task_delete(request):
    if request.method == "POST":
        id = request.POST['taskId']
        print(id)
        task = get_object_or_404(Task, id=id)
        task.delete()
    return HttpResponse("remove")


@csrf_exempt
def task_create(request):

    if not request.user.is_authenticated:
        return HttpResponse("UserNotLogin")
    if request.method == "POST":
        taskName = request.POST['taskName']
        tags = request.POST.getlist('selectedTags')
        UserData = request.user
        array = []
        tagsZero = tags[0]  # string'e döndürdük, split kullanabilmek için
        count = tagsZero.count('&')
        for i in range(count + 1):
            elements = tagsZero.split('&')[i]
            arrayValues = elements[5:]
            array.append(arrayValues)
        print(array)
        print(tags)
        Task.objects.create(task=taskName,is_completed=False,user=UserData)
        latestData = Task.objects.latest('id')
        for x in (array):
           if x == "priority":
             print("Önceliklii")
             TagsTaskIntegration.objects.create(task_id=latestData.id,tag_id=1)
           elif x == "normal":
               TagsTaskIntegration.objects.create(task_id=latestData.id,tag_id=2)
           elif x == "work":
               TagsTaskIntegration.objects.create(task_id=latestData.id,tag_id=3)
        return HttpResponse("create")
    #    task = get_object_or_404(Task, id=id)
    #    task.delete()

@csrf_exempt
def task_stateUpdate(request):
    if not request.user.is_authenticated:
        return HttpResponse("UserNotLogin")
    if request.method == "POST":
        taskState = request.POST['taskState']
        taskId = request.POST['taskId']
        task = get_object_or_404(Task, id=taskId)
        task.is_completed = taskState
        task.save()
    return HttpResponse("update")

