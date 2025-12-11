# django_crud/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Importar las vistas de la API (TaskViewSet)
from .api_views import TaskViewSet 
# Importar las vistas basadas en plantillas (CRUD HTML)
from . import views 

# 1. ¡CORRECCIÓN CLAVE! Define el nombre de la aplicación
app_name = 'crud'

# Configuración del Router de la API
router = DefaultRouter()
router.register(r'tasks', TaskViewSet) 

urlpatterns = [
    # A. URLS DE LA API (Generalmente bajo '/api/')
    # Las rutas generadas por router.urls son: /tasks/, /tasks/<pk>/, etc.
    path('api/', include(router.urls)),

    # B. URLS BASADAS EN PLANTILLAS (Para tu CRUD HTML/Django anterior)
    # Estas son las que necesitas para que funcione el 'redirect' y la vista inicial
    path('', views.task_list_and_create, name='crud_list'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]