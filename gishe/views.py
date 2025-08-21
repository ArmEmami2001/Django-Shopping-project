from django.shortcuts import render


# Create your views here.
#request handler for managing the requests
def signin(request):
    return render(request,'signin.html')