from django.urls import path, re_path
from .import views

from .views import ThreadView, InboxView

app_name = 'chat'
urlpatterns = [
    path("", InboxView.as_view(), name='inbox'),
    re_path(r"^(?P<username>[\w.@+-]+)/$", ThreadView.as_view(),name = "chatur1"),
    path('profile',views.profile, name = 'profile'),
    path('register',views.register,name='register'),
    path('user_login',views.user_login,name='user_login'),
    path('user_logout',views.user_logout,name='user_logout'),
]