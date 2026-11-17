from django.urls import path
from . import views

urlpatterns = [
    path('', views.TerneroListView.as_view(), name='catalogo'),
    path('ternero/<int:pk>/', views.TerneroDetailView.as_view(), name='detalle'),
    path('ternero/nuevo/', views.TerneroCreateView.as_view(), name='crear'),
    path('ternero/<int:pk>/editar/', views.TerneroUpdateView.as_view(), name='editar'),
    path('ternero/<int:pk>/eliminar/', views.TerneroDeleteView.as_view(), name='eliminar'),
]