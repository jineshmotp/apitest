# urls.py

from django.contrib import admin
from django.urls import path
from .views import ProjectListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/projects/', ProjectListView.as_view(), name='project-list'),
    path('api/project/<int:project_id>/', ProjectListView.as_view(), name='project-detail'),
    path('api/projects/create/', ProjectListView.as_view(), name='create-project'),
    path('api/projects/<int:project_id>/', ProjectListView.as_view(), name='update-project'),  
    
]
