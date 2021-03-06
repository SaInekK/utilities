from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django.contrib import messages

from .models import TaskModel


class TaskListView(LoginRequiredMixin, ListView):
    login_url = "login"
    model = TaskModel
    template_name = 'todos/tasks.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['incomplete_tasks'] = context['tasks'].filter(completed=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                Q(title__icontains=search_input) |
                Q(description__icontains=search_input))
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    login_url = "login"
    model = TaskModel
    template_name = 'todos/task_detail.html'
    context_object_name = 'task'


class CreateTaskView(LoginRequiredMixin, CreateView):
    login_url = "login"
    model = TaskModel
    template_name = 'todos/create_task.html'
    fields = ['title', 'description', 'image', 'completed']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTaskView, self).form_valid(form)


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    model = TaskModel
    template_name = 'todos/update_task.html'
    fields = ['title', 'description', 'image', 'completed']
    success_url = reverse_lazy('tasks')

    # def form_valid(self, form):
    #     messages.success(self.request, f"The record was updated!")
    #     return super(UpdateTaskView, self).form_valid(form)


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    model = TaskModel
    template_name = 'todos/delete_task.html'
    success_url = reverse_lazy('tasks')
    context_object_name = 'task'
