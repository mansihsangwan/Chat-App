from django.urls import path, re_path
from .import views

from .views import ThreadView, InboxView

app_name = 'chat'
urlpatterns = [
    path("", InboxView.as_view()),
    re_path(r"^(?P<username>[\w.@+-]+)/$", ThreadView.as_view(),name = "chatur1"),
    path('home',views.profile, name = 'profile')
]