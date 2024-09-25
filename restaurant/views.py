from django.shortcuts import render
import random

# Create your views here.
def base(request):
    '''display the base page of the restaurant'''
    template_name = 'restaurant/base.html'
    return render(request,template_name)

def main(request):
    '''display the main page of the restaurant'''
    template_name = 'restaurant/main.html'
    return render(request,template_name)



def order(request):
    '''display the order page of the restaurant'''
    template_name = 'restaurant/order.html'
    specialList = ['Fish - $5.00', 'Noddles - $5.00', 'Soup - $5.00', 'Pancake - $5.00']
    context ={
        'special' : specialList[random.randint(0,3)]
    }
    return render(request,template_name,context)


def confirmation(request):
    
    '''
    display confirmation page
    '''
    template_name = 'restaurant/confirmation.html'
    if request.POST:
        menu1 = request.POST.get('menu1')
        menu2 = request.POST.get('menu2')
        menu3 = request.POST.get('menu3')
        menu4 = request.POST.get('menu4')
        sp1 = request.POST.get('sp1')
        sp2 = request.POST.get('sp2')
        sp3 = request.POST.get('sp3')
        special = request.POST.get('special')
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        instructions = request.POST['instructions']
        spicy = []
        orderList = []
        sumOrder = 0
        if sp1 == 'no spicy':
            spicy.append(sp1)
        if sp2 == 'mild':
            spicy.append(sp2)
        if sp3 == 'hot':
            spicy.append(sp3)
            
            
            
        if menu1 == 'KongPaoChicken':
            orderList.append(menu1)
            sumOrder = sumOrder + 13
        if menu2 == 'OrangeDuck': 
            orderList.append(menu2)   
            sumOrder = sumOrder + 12
        if menu3 == 'TofuVegetable':  
            orderList.append(menu3)  
            sumOrder = sumOrder + 18
        if menu4 == 'WongTong':   
            orderList.append(menu4) 
            sumOrder = sumOrder + 11
        if special == 'Fish - $5.00' or special == 'Noddles - $5.00' or special == 'Soup - $5.00' or special == 'Pancake - $5.00':
            orderList.append(special)
            sumOrder +=5    
            
        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'sumOrder': sumOrder,
            'menu1': menu1,
            'menu2': menu2,
            'menu3': menu3,
            'menu4': menu4,
            'special': special,
            'instructions': instructions,
            'orderList': orderList,
            'spicy': spicy,
 
        }


    
    return render(request,template_name,context=context)




    