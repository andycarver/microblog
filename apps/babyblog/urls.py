from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_reg$', views.login_reg, name='login_reg'),
    url(r'^babytwitter$', views.babytwitter, name='babytwitter'),
    url(r'^tweet$', views.tweet, name='tweet'),
    url(r'^destroy/(?P<id>\d+)$', views.destroy),
    url(r'^logout$', views.logout, name='logout')
]
