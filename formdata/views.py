from django.shortcuts import render

# Create your views here.
def show_form(request):
    '''show form to client'''
    template_name = 'formdata/form.html'
    return render(request,template_name)
    
    
def submit(request):
    '''handle the submit here: read the form data, generate a response'''
    
    template_name = 'formdata/confirmation.html'
    
    #read the form data
    #check if the request is a POST
    if request.POST:
        name = request.POST['name']
        favorite_color = request.POST['favorite_color'] 
        #package the data back up to be used in the response
        context = {
            'name' : name,
            'favorite_color': favorite_color,
        }   
    
    #generate a response
    
    return render(request,template_name, context)

   