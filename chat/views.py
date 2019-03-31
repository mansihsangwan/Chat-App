from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404,HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.contrib.sessions.models import Session
from django.views.generic import DetailView, ListView
from django.views import generic
from .forms import ComposeForm, UserListForm, UserForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


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



def profile(request):
    if request.user.is_superuser:
        list = User.objects.all()
        status = Status.objects.all()
        context = {'users':list, 'status':status}
        return render(request,'home1.html',context)
    return render(request,'chat/thread.html',{})


def index(request):
    #Session.objects.all().delete()
    user_sessions = Session.objects.all()
    context ={'user_sessions': user_sessions }
    return render(request,'index1.html', context)

@login_required
def special(request):
    

    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    statuss= Status.objects.filter(user = request.user)
    
    for status in statuss:
        status.session.all().delete()
        """ status_instance = Status.objects.get(user = request.user)
        status_instance.online = 0
        status_instance.save() """
    logout(request)
       
    return HttpResponseRedirect(reverse('index'))

    

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
        
    return render(request,'registration.html',
                          {'user_form':user_form,
                           
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print ('First call: is expired at the browser close', request.session.get_expire_at_browser_close() )

        user = authenticate(username=username, password=password)
        
          
            
        if user:
            
            if user.is_active:
                login(request,user)
               
                status_instance = Status.objects.get_or_create(user = request.user, session_id = request.session.session_key)
                status_instance = Status.objects.get(user = request.user, session_id = request.session.session_key)
               
                status_instance.save()
                return HttpResponseRedirect(reverse('index'))             
                   
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        #request.session.set_expiry(settings.LOGIN_SESSION_TIMEOUT) 
        #settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # just to makie sure          
        #print ('Second call: is expired at the browser close', request.session.get_expire_at_browser_close())
        return render(request, 'login.html', {})


