from django.conf.urls import url
from rango import views
from django.contrib import admin

urlpatterns = [
    url(r'^index$',views.index,name = 'index'),
    url(r'^admin/', admin.site.urls),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category, name='show_category'),

]