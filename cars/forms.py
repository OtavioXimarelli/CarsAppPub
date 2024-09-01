from django import forms
from cars.models import Car

class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

    def validate_field(self, field_name, min_value, error_message):
        value = self.cleaned_data.get(field_name)
        if value < min_value:
            self.add_error(field_name, error_message)
        return value

    def clean_factory_year(self):
        return self.validate_field('factory_year', 1920, 'Não é possível adicionar carros com fabricação anterior ao ano 1920')

