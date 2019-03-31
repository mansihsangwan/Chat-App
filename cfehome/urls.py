from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from chat import views

urlpatterns = [
    #path('', TemplateView.as_view(template_name="home.html")),
    path('admin/', admin.site.urls),
    path('messages/', include('chat.urls')),
    path('',views.index,name='index'),
    path('special',views.special,name='special'),
    path('session_security', include('session_security.urls')),
    path('logout', views.user_logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

"""urlpatterns += [
    path('', RedirectView.as_view(url='/messages/profile', permanent=True)),
]"""