from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^my_stocks/$', views.my_stock_list),
    url(r'^my_stocks/create/$', views.my_stock_create),
    url(r'^all_stock_fundamentals/$', views.all_stock_fundamental_list),
    url(r'^all_stocks/$', views.all_stock_list),
    url(r'^recommend_stocks/$', views.recommend_stock_list),
    url(r'^recommend_stocks_by_strategies/$', views.recommend_stock_list),
    url(r'^manual_recommend_stocks/create/$', views.manual_recommend_stock_create),
    url(r'^manual_recommend_stocks/$', views.manual_recommend_stocks),
    url(r'^recommend_industries/$', views.recommend_industry_list),
    url(r'^daily_limit_stocks/$', views.daily_limit_stocks),
]