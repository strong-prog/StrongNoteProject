from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import Notes, Category, Comment
from .forms import UserRegisterForm, UserLoginForm, CommentForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация успешна!')
            user = form.save()
            login(request, user)
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = UserRegisterForm()
    return render(request, 'Notes/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Home')
    else:
        form = UserLoginForm()
    return render(request, 'Notes/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('Login')


class HomeNotes(ListView, Paginator):
    model = Notes
    context_object_name = 'notes'
    template_name = 'Notes/home.html'
    extra_context = {'title': 'Главная'}
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Notes.objects.filter(is_published=True).select_related('category')


class NotesByCategory(ListView, Paginator):
    model = Notes
    template_name = 'Notes/home.html'
    context_object_name = 'notes'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return Notes.objects.filter(category_id=self.kwargs['category_id'],
                                    is_published=True).select_related('category')


class ViewNotes(DetailView):
    model = Notes
    template_name = 'Notes/view_notes.html'
    context_object_name = 'notes_item'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = Comment.objects.filter(
            note_connected=self.get_object()).order_by('-created')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(text=request.POST.get('text'),
                              username=self.request.user,
                              note_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)
