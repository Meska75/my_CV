from django.urls import path
from my_cv.views import (
    ai_chat_view,
    decoy_admin_view,
    index_view,
    project_detail_view,
    resume_view,
)

app_name = 'my_cv'

urlpatterns = [
    path('', index_view, name='index'),
    path('resume/', resume_view, name='resume'),
    path('projects/<str:slug>/', project_detail_view, name='project_detail'),
    path('ai_chat_view', ai_chat_view, name='ai_chat_view'),
    path('admin/', decoy_admin_view, name='decoy_admin'),
]
