from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Server
from .forms import ServerForm
from .aes4  import enc, dec, enczip

@login_required
def dashboard(request):
    if request.method == 'POST':
        data = request.POST['idnum']
        servers=Server.objects.filter(server_name__contains = data , user=request.user ).order_by('id')
        return render(request, 'servers/dashboard.html', {'servers': servers, 'data':data })
    else:
        servers=Server.objects.filter(user=request.user).order_by('id')
        return render(request, 'servers/dashboard.html', {'servers': servers, 'data':''})
    servers = Server.objects.filter(user=request.user)
    return render(request, 'servers/dashboard.html', {'servers': servers})
    
@login_required
def signout(request):
    logout(request)
    return redirect('/login/')

@login_required
def add_server(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            server = form.save(commit=False)
            server.user = request.user
            server.password = enc(form.cleaned_data['password'],form.cleaned_data['keytext'])
            server.config_bin = enczip(form.cleaned_data['config_text'],form.cleaned_data['keytext'])
            form.save()
            return redirect('dashboard')
    else:
        form = ServerForm()
    return render(request, 'servers/add_server.html', {'form': form , 'title': 'Add Pass'})

@login_required
def edit_server(request, pk):
    server = get_object_or_404(Server, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ServerForm(request.POST, instance=server)        
        if form.is_valid():
            server = form.save(commit=False)
            server.user = request.user
            server.password = enc(form.cleaned_data['password'],form.cleaned_data['keytext'])
            if form.cleaned_data['config_text']:
                server.config_bin = enczip(form.cleaned_data['config_text'],form.cleaned_data['keytext'])
            form.save()
            return redirect('dashboard')
    else:
        form = ServerForm(instance=server)
    return render(request, 'servers/add_server.html', {'form': form , 'title': 'Edit Pass'})

@login_required
def delete_server(request, pk):
    server = get_object_or_404(Server, pk=pk, user=request.user)
    if request.user:
        server.delete()
    return redirect('dashboard')

@login_required
def download_config(request, pk):
    server = get_object_or_404(Server, pk=pk, user=request.user)
    response = HttpResponse(server.config_bin, content_type='application/zip')
    response['Content-Disposition'] = f'inline;filename={server.server_name}_config.zip'
    return response

@login_required
def get_pass_str(request):
    pass_str = '(Password Not Found)'
    if request.method == 'POST':
        try:
            idx = request.POST['idx']
            key = request.POST['key']
            server = get_object_or_404(Server, pk=idx, user=request.user)
            pass_str = dec(server.password,key)
        except:
            return HttpResponse('(Password Not Found)', content_type='text/plain')
    return HttpResponse(pass_str, content_type='text/plain')

@login_required
def checkpass(request):
    res = 'NotOK'
    if request.method == 'POST':        
        password = request.POST['pass']
        if check_password(password,request.user.password):
            res='OK'       
    return HttpResponse(res, content_type='text/plain')




        
