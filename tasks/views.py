from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404
from tasks.models import Task
from tags.models import *
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
import datetime


# Create your views here.

def task_index(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
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
        return redirect('/accounts/login')
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
        return redirect('/accounts/login')
    if request.method == "POST":
        taskState = request.POST['taskState']
        taskId = request.POST['taskId']
        task = get_object_or_404(Task, id=taskId)
        task.is_completed = taskState
        task.save()
    return HttpResponse("update")


def get_PDF(request):

    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    user = User.objects.get(id=request.user.id)
    tasks = user.tasks.all()
    taskTagIntegration = TagsTaskIntegration.objects.all()
    tags = Tag.objects.all()

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(50,800,"TASKS")
    p.drawString(260, 800, "TAGS")
    p.drawString(370, 800, "COMPLETED")
    p.drawString(480, 800, "CREATED TIME")
    ycoordinate = 770
    for x in tasks:
        x_coordinate_for_tags = 220
        for y in taskTagIntegration:
            if x.id==y.task_id:
                if y.tag_id==1:
                    p.drawString(x_coordinate_for_tags, ycoordinate, "Priority")
                    x_coordinate_for_tags = x_coordinate_for_tags + 50
                elif y.tag_id==2:
                    p.drawString(x_coordinate_for_tags, ycoordinate, "Normal")
                    x_coordinate_for_tags = x_coordinate_for_tags + 50
                elif y.tag_id==3:
                    p.drawString(x_coordinate_for_tags, ycoordinate, "Work")
                    x_coordinate_for_tags = x_coordinate_for_tags + 50
        date_time = x.created_at.strftime("%m/%d/%Y, %H:%M")
        if x.is_completed == 1:
            p.drawString(400, ycoordinate, "✓")
        else:
            p.drawString(400, ycoordinate, "No")
        p.drawString(20, ycoordinate, x.task) # x koordinatı, y koordinatı
        p.drawString(470, ycoordinate, date_time)
        ycoordinate = ycoordinate - 25
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    file_name = user.get_username() + '-' +  datetime.datetime.now().strftime("%m%d%Y%H%M") + '.pdf'
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=file_name)

