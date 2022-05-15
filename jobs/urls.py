from django.urls import path
from . import views


urlpatterns = [
    path('find_jobs/', views.find_jobs, name='find_jobs'),
    path('profile/', views.profile, name='profile'),
    path('get_job/<int:id>/', views.get_job, name='get_job'),
    path('profile/send_work/', views.send_work, name='send_work'),
    path('create_job/', views.create_job, name='create_job'),
    path('update_job/<int:job_id>/', views.update_job, name='update_job'),
    path('confirm_delete/<int:job_id>/', views.confirm_delete, name='confirm_delete'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
]
