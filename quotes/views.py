from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.
quoteList = ['What can I say, Mamba Out!', 'I am the chosen one', 'you must first learn to fail']
imgList = [ '/static/kobe.jpg', '/static/lbj.jpg', '/static/mj.jpg']
personList = ['This is Kobe from LA Lakers', 'This is LBJ the king from LA Lakers', 'Michal Jordan from Bulls, the greatest ever']


def base(request):
    global num
    num = random.randint(0,2)
    template_name = "quotes/base.html"
    # create a dictionary of context variables
    context = {
        'quote' : quoteList[num],
        'image' : imgList[num],
    }
    return render(request, template_name, context)


def quote(request):
    global num
    template_name = "quotes/quote.html"
    # create a dictionary of context variables
    context = {
        'quote' : quoteList[num],
        'image' : imgList[num],
    }
    return render(request, template_name, context)

def show_all(request):
    template_name = "quotes/show_all.html"
    # create a dictionary of context variables
    context = {
         'quote' : quoteList,
        'image' : imgList,
    }
    return render(request, template_name, context)

def about(request):
    global num
    template_name = "quotes/about.html"
    # create a dictionary of context variables
    context = {
        'person': personList[num],
    }
    return render(request, template_name, context)