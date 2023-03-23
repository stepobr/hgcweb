from django.shortcuts import render

def cassettes(request):
    return render(request, 'cassettes_index.html')