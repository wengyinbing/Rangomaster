from django.conf.urls import url
from rango import views
from django.contrib import admin


app_name = 'rango'
urlpatterns = [
    url(r'^index$',views.index,name = 'index'),
    url(r'^admin/', admin.site.urls),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category, name='show_category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^register/$',views.register,name='register'), # 新增的模式
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^search/$', views.search, name='search'),
    url(r'^track_url$', views.track_url, name='track_url'),
]