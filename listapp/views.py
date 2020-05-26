from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from .decorators import *

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            l_user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customers')
            l_user.groups.add(group)
            customer = Customer()
            customer.user = l_user
            customer.name = username
            customer.save()

            print('#################################################')
            print(username)
            print(l_user.customer)
            familia = Familia()
            familia.name = username+"_personal"
            familia.save()
            familia.miembro.add(customer)
            familia.save()

            print(familia, familia.miembro.all())

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'listapp/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            print('COMPANYERO')
            return redirect('profile')
        else:
            messages.info(request,'Username OR Password is incorrect')
    return render(request, 'listapp/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request,'listapp/home.html')

def profilePage(request):
    l_user = request.user
    print('########################################################################################')
    print('USER: ', l_user)
    l_customer = request.user.customer
    familias = l_customer.familia_set.all()
    listas = []
    print(familias)
    for familia in familias:
        for lista in familia.lista.all():
            listas.append(lista)
    context = {'user':l_user, 'customer':l_customer, 'familias':familias, 'listas':listas}
    return render(request, 'listapp/profile.html', context)

def congrats(request):
    return render(request,'listapp/congrats.html')

def familia(request, pk):
    familia = Familia.objects.get(id = pk)
    if request.user.customer in familia.miembro.all():
        listas = familia.lista.all()
        miembros = familia.miembro.all()
        print(familia, familia.name)
        context = {'listas':listas, 'miembros':miembros, 'familia':familia}
        return render(request, 'listapp/familia.html', context) 
    else:
        return redirect('profile')

def lista(request, pk):
    la_lista = Lista.objects.get(id=pk)
    items = la_lista.item.all()
    la_lista.save()

    context = {'lista':la_lista.name, 'items':items}
    if request.method =='POST':
        if request.POST.get('name'):
            new_item= Item()
            new_item.name = request.POST.get('name')
            new_item.status = 'Por comprar'
            if request.POST.get('adinfo'):
                new_item.aditional_info = request.POST.get('adinfo')

            new_item.save()
            la_lista.save()
            la_lista.item.add(new_item)
            la_lista.save()
        if request.POST.get('compra'):
            pd = int(request.POST.get('compra'))
            c_item = la_lista.item.get(id = pd)
            c_item.status = 'Comprado'
            c_item.save()
        if request.POST.get('delete'):
            pd = int(request.POST.get('delete'))
            la_lista.item.remove(pd)
            la_lista.save()

    return render(request,'listapp/lista.html',context)

def new_lista(request):
    customer = request.user.customer
    familias = customer.familia_set.all()
    print('FAMILIAS', familias)
    pf_id = customer.familia_set.get(name = customer.name + '_personal').id
    if request.method == 'POST':
        if request.POST.get('familia'):
            f_id= request.POST.get('familia')
        else:
            f_id = request.user.customer.familia_set(name = customer.name + '_personal').id
        if request.POST.get('name'):
            name = request.POST.get('name')
        else:
            name = 'untitled'

        lista = Lista()
        lista.name = name
        familia = Familia.objects.get(id = f_id)
        lista.save()
        familia.save()
        familia.lista.add(lista)
        return redirect('/lista/'+str(lista.id))
    
    context = {'familias':familias}
    return render(request, 'listapp/new_lista.html', context)

def login2(request):
    return render(request,'listapp/login.html')
