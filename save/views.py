from django.shortcuts import render

from .models import Saved

# Create your views here.


def saved_item(request):
    items = Saved.objects.filter(user=request.user)
    return render(request, 'save/saved_item.html', {'items':items})