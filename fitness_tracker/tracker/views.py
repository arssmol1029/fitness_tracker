from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm 
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    name = request.user.username
    return render(request, 'tracker/dashboard.html', {'name': name})

def signup(request):
    # Если пользователь уже авторизован, перенаправляем его
    if request.user.is_authenticated:
        return redirect('dashboard')  # Замени 'dashboard' на свою главную страницу

    # Если форма отправлена (POST-запрос)
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Связываем данные с формой
        if form.is_valid():  # Проверяем валидность
            user = form.save()  # Сохраняем пользователя (вызывается метод save() из формы)
            login(request, user)  # Автоматически входим под новым пользователем
            return redirect('dashboard')  # Перенаправляем на главную
    else:
        form = SignUpForm()  # Пустая форма для GET-запроса

    # Рендерим шаблон с формой
    return render(request, 'registration/signup.html', {'form': form})