from django.shortcuts import render

# Create your views here.
def password_generator(request):
    return render(request, "passgen.html")
