from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from braces.views import LoginRequiredMixin


from .models import Medicamento
from .forms import MedicamentoForm

class Registrar(LoginRequiredMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'medicamentos/registrar.html'
    success_url = reverse_lazy('medicamentos:listado')

    def form_valid(self, form):
        form.save()
        return super(Registrar, self).form_valid(form)

class Listado(LoginRequiredMixin, ListView):
    context_object_name = "medicamentos"
    template_name = 'medicamentos/listado.html'

    def get_queryset(self):
        return Medicamento.obtener_listado()

class Modificar(LoginRequiredMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'medicamentos/modificar.html'
    success_url = reverse_lazy('medicamentos:listado')