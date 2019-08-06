from django import forms
from django.contrib.auth.models import Group
from django.forms import CheckboxSelectMultiple

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name", "permissions",)
        widgets = {
            "permissions": CheckboxSelectMultiple,
        }

    def label_from_instance(self, obj):
        return "%s" % obj.name

    def __init__(self, *args, **kwargs):
        from django.db.models import Case, When

        from .listado_permisos import LISTADO_PERMISOS

        super(GrupoForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = "Nombre*"
        orden_permisos = Case(*[When(codename=codename, then=pos) for pos, codename in enumerate(LISTADO_PERMISOS)])
        self.fields["permissions"].queryset = self.fields["permissions"].queryset.filter(codename__in=LISTADO_PERMISOS).order_by(orden_permisos)
        self.fields['permissions'].label_from_instance = self.label_from_instance