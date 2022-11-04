from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^stocks/$', views.stock_list, name='article_page'),
]