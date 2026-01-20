from django.http import HttpResponse

def conventions_home(request):
    return HttpResponse("Module conventions OK")
