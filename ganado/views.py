from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Ternero
from .forms import TerneroForm

# 1. Catálogo (Público, optimizado con select_related)
class TerneroListView(ListView):
    model = Ternero
    template_name = 'ganado/catalogo.html'
    context_object_name = 'terneros'
    
    def get_queryset(self):
        return Ternero.objects.select_related('raza').all()

# 2. Detalle (Público)
class TerneroDetailView(DetailView):
    model = Ternero
    template_name = 'ganado/detalle.html'
    context_object_name = 'ternero'

# 3. Crear (Protegido con LoginRequiredMixin)
class TerneroCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ternero
    form_class = TerneroForm
    template_name = 'ganado/formulario.html'
    success_url = reverse_lazy('catalogo')
    success_message = "El ternero %(numero_identificador)s fue registrado exitosamente."

# 4. Editar (Protegido con LoginRequiredMixin)
class TerneroUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ternero
    form_class = TerneroForm
    template_name = 'ganado/formulario.html'
    success_url = reverse_lazy('catalogo')
    success_message = "El ternero %(numero_identificador)s fue actualizado correctamente."

# 5. Eliminar (Protegido con LoginRequiredMixin)
class TerneroDeleteView(LoginRequiredMixin, DeleteView):
    model = Ternero
    template_name = 'ganado/confirmar_eliminar.html'
    success_url = reverse_lazy('catalogo')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f"El ternero {obj.numero_identificador} fue eliminado del sistema.")
        return super().delete(request, *args, **kwargs)