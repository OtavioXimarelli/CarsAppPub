from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from cars.models import Car
from cars.forms import CarModelForm


class CarListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'
    ordering = ['model']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if search_query := self.request.GET.get('search'):
            queryset = queryset.filter(model__icontains=search_query)
        return queryset
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/cars/'
    

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'
    
    def get_success_url(self):
        return reverse_lazy('car_details', kwargs={ 'pk': self.object.pk})
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'