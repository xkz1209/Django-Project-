from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.
quoteList = ['What can I say, Mamba Out!', 'I am the chosen one', 'you must first learn to fail']
imgList = [ '/static/kobe.jpg', '/static/lbj.jpg', '/static/mj.jpg']
personList = [' NBA All-Defensive Second Team /  NBA scoring champion / NBA Slam Dunk Contest /NBA All-Rookie Second Team', 'NBA 75th Anniversary Team / All-NBA First Team / NBA All-Rookie Second Team/Fourth-team Parade All-American  ', 'NBA 75th Anniversary Team / All-NBA First Team /NBA All-Rookie Second Team /NBA All-Star Game MVP']


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
    template_name = "quotes/about.html"
    # create a dictionary of context variables
    context = {
        'person': personList[num],
    }
    return render(request, template_name, context)