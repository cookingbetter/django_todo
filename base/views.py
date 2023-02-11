from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
'''LoginRequiredMixin means if user is not loged in 
    then user will be redirected to  "watch settings.LOGIN_URL"'''

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    # if user is authenticated, we redirect him to the page
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')    #  when user logs in we want send him to 'tasks' page


class RegisterRage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterRage, self).form_valid(form)

    def get(self, *args, **kwards):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterRage, self).get(*args, **kwards)


class TaskList(LoginRequiredMixin, ListView):
    # using LoginRequiredMixin. watch above
    model = Task
    context_object_name = 'tasks'       # instead of object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)      # every user can see only his tasks
        context['count'] = context['tasks'].filter(complete=False).count()

        # if in form happens get
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                # title__startswith=search_input) 
                title__icontains=search_input) 

        context['search_input'] = search_input

        return context



class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'        # instead of object
    template_name = 'base/task.html'    # instead of task_detail name


class TaskCreate(LoginRequiredMixin, CreateView):
    # it gives a form with exact field
    model = Task
    fields = ['title', 'description', 'complete']       # '__all__'
    """goes to 'task_list.html'. 
    But why? 
    We do not use template_name = 'base/tasks.html', 
    only context_object_name = 'tasks'"""
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        # model.user automatically fills with current user 
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    '''just copy TaskCreate functional'''
    model = Task
    fields = ['title', 'description', 'complete']  
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


def show_map(request):
    return render(request, 'map.html')