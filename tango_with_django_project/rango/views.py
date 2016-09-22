from django.shortcuts import render
from django.http import HttpResponse
from rango import models

# Create your views here.

def index(request):
    category_list = models.Category.objects.order_by('-likes')[:5]

    context_dict = {'categories': category_list}
    return render(request, 'rango/index.html',context=context_dict)


def about(request):
    context_dict = {'authorname': "Nick Hess"}
    return render(request, 'rango/about.html', context=context_dict)