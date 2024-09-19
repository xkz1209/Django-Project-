from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
#descri: the logic handle URL requests
# Create your views here.

# def home(request):
#     '''A function to respond to the /hw URL.'''
#     response_text = f'''
#     <html>
#     <h1>hello,world!</h1>
#     <table>
#     <tr> <td> {time.ctime()}</td>    </tr>
#     <table>
#     <hr>
#     <html>
    
#     ''' # create some text
    
#     return HttpResponse(response_text) # return a response to the client

def home(request):
    '''
    a function to respond to the /hw url
    delegate 
    '''
    
    template_name = "hw/home.html"
    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'letter1' : chr(random.randint(60,90)), 
        'letter2' : chr(random.randint(60,90)), # a letter in the range A...Z
        'number': random.randint(1,10), # a number in the range 1...10
    }
    return render(request, template_name, context)