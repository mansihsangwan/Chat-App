from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView
from django.views import generic
from .forms import ComposeForm, UserListForm
from .models import Thread, ChatMessage
from django.contrib.auth.models import User



class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form_class =self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.get('thumb')
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        thumb = form.cleaned_data.get("thumb")
        ChatMessage.objects.create(user=user, thread=thread, message=message, thumb=thumb)
        return super().form_valid(form)

"""class UserListView(generic.ListView):
    model = ChatMessage
    context_object_name = 'my_user_list'
    queryset = ChatMessage.objects.all()
    template_name = 'home.html'"""

def profile(request):
    list = User.objects.all()
    context = {'users':list}

    return render(request,'home.html',context)