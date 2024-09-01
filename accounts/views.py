from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        registration_form = UserCreationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            messages.success(request, 'Usuário registrado com sucesso!')
            return redirect('cars_list')
    else:
        registration_form = UserCreationForm()  # Use the same form instance
    return render(request, 'register.html', {'registration_form': registration_form})

def login_view(request):
    if request.method == "POST":
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'Logado com sucesso!')
            return redirect('cars_list')
        else:
            messages.error(request, 'Usuário não encontrado')
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})
    
def logout_view(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso!')
    return redirect('cars_list')