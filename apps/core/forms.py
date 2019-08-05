from django import forms

class ContactanosForm(forms.Form):
    nombre = forms.CharField(label="Nombre*")
    email = forms.EmailField(label="Correo electrónico*")
    telefono = forms.CharField(label="Teléfono/Celular*")
    mensaje = forms.CharField(widget=forms.Textarea, label="Mensaje*")

    def __init__(self, *args, **kwargs):
        super(ContactanosForm, self).__init__(*args, **kwargs)
        self.fields['mensaje'].widget.attrs['rows'] = 5
        self.fields['mensaje'].widget.attrs['style'] = 'resize:none'