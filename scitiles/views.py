from django.shortcuts import render

def scitiles(request):
    return render(request, 'tiles_index.html')
