from django.urls import path
from . import views


urlpatterns = [
    path('find_jobs/', views.find_jobs, name='find_jobs'),
    path('profile/', views.profile, name='profile'),
    path('get_job/<int:id>/', views.get_job, name='get_job'),
    path('profile/send_work/', views.send_work, name='send_work'),
    path('create_job/', views.create_job, name='create_job'),
]
