from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from .models import Record
from django.contrib import messages


# Create your views here.

def home(request):
    # return HttpResponse("Home Page")
    return render(request, 'webapp/index.html')


def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('my-login')
            
    
    context = {'form':form}
    return render(request, 'webapp/register.html', context=context)

def my_login(request):
    form = LoginForm()
    if request.method=='POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password= password)
            
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    context = {'form':form}
    return render(request, 'webapp/my-login.html', context=context)
    
    
    
    
@login_required(login_url='my-login')
def dashboard(request):
    my_record = Record.objects.all()
    context= {'records':my_record}
    return render(request, 'webapp/dashboard.html', context=context)
    
    


@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record created successfully!')
            
            return redirect('dashboard')
    context= {'form':form}
    return render(request, 'webapp/create-record.html', context=context)

@login_required(login_url='my-login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully!')
            return redirect('dashboard')
    context= {'form':form}
    return render(request, 'webapp/update-record.html', context=context)

@login_required(login_url='my-login')
def view_record(request, pk):
    all_record = Record.objects.get(id=pk)
    context= {'record':all_record}
    return render(request, 'webapp/view-record.html', context=context)

@login_required(login_url='my-login')
def delete_record(request, pk):
    delete_record = Record.objects.get(id=pk)
    delete_record.delete()
    messages.success(request, 'Record deleted successfully!')
    
    return redirect('dashboard')




def user_logout(request):
    auth.logout(request)
    messages.success(request, 'Logout successfully!')
    
    return redirect("my-login")
        