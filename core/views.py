from django.http import HttpResponse

def home(request):
    return HttpResponse("Home OK (projet stages)")
