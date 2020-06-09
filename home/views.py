from django.shortcuts import render, HttpResponse

# Create your views here.

def home_view(request):
    context = {
        'isim': 'Said',
    }
    return HttpResponse('<br>Hoşgeldiniz</b>')
    #return render(request, 'index.html',context)