"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from rango import views
from registration.backends.simple.views import RegistrationView

# 定义一个类
# 用户成功注册后重定向到首页
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/index/'


urlpatterns = [
    #path('admin/', admin.site.urls),
    #path("",index ,name = 'index')
    url(r'^$',views.index,name='index'),
    url(r'^admin/',admin.site.urls),
    url(r'^rango/',include('rango.urls')),
    url(r'^accounts/register/$',MyRegistrationView.as_view(),name='registration_register'),
    #上面把rango开头的交给rango应用处理
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^registration/logout$',views.logout,name='logout')
]
