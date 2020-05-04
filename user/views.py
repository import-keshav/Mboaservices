from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import User
from .forms import UserForm


class UserListView(ListView):
    model = User


class UserCreateView(CreateView):
    model = User
    form_class = UserForm


class UserDetailView(DetailView):
    model = User


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm

