# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import NewUserForm, PostForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Post


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Успешная регистрация.")
            return redirect("homepage")
        messages.error(request, "Ошибка при регистрации, попробуйте еще раз.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_req(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Теперь вы вошли как {username}.")
                return redirect("homepage")
            else:
                messages.error(request, "Неверный логин/пароль.")
        else:
            messages.error(request, "Неверный логин/пароль.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def homepage(request):
    context = {}
    context['posts'] = Post.objects.all().order_by('-id')
    if request.method == 'POST' and 'pk' in request.POST:
        Post.objects.filter(id=request.POST['pk']).delete()
        messages.success(request, 'Пост успешно удален!')
        return redirect('/')
    return render(request=request, template_name="homepage.html", context=context)


def logout_req(request):
    logout(request)
    messages.info(request, "Вы успешно вышли из системы.")
    return redirect("homepage")


def create_post(request):
    if not request.user.is_superuser:
        return redirect('/')
    context = {}
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успешно добавлен!')
            return redirect('/')
    form = PostForm()
    context['form'] = form
    return render(request, 'create_post.html', context)


def edit_post(request, pk):
    if not request.user.is_superuser:
        return redirect('/')
    context = {}
    item = Post.objects.get(id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успешно изменен!')
            return redirect('/')
    context['form'] = PostForm(instance=item)
    return render(request, 'edit_post.html', context)


def view_post(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'Для просмотра необходимо авторизоваться на сайте')
        return redirect('/login')
    context = {}
    item = Post.objects.get(id=pk)
    context['post'] = item
    return render(request, 'view_post.html', context)

