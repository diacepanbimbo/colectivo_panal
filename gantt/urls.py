from django.conf.urls import url

from . import views

app_name = 'gantt'
urlpatterns = [
    # ex: /polls/
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^project/$', views.project),
    url(r'^modify_project/$', views.modify_project),

    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),


]
