from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'tasks/(?P<task_id>[0-9]+)/$', views.task, name='task'),
    url(r'tasks/$', views.tasks, name='tasks'),
    url(r'people/(?P<person_id>[0-9]+)/$', views.person, name='person'),
    url(r'people/$', views.people, name='people'),
    url(r'country/(?P<country_id>[a-z]+)/$', views.country, name='country'),
    url(r'hall-of-fame/$', views.hall_of_fame, name='hall-of-fame'),
    url(r'(?P<olympiad_id>[0-9]+)/$', views.olympiad, name='olympiad'),
    url(r'(?P<olympiad_id>[0-9]+)/ranking/$', views.ranking, name='ranking'),
    url(r'$', views.olympiads, name='olympiads'),
]
