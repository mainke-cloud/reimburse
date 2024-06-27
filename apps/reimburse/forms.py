from django import forms
from crispy_formset_modal.helper import ModalEditFormHelper
from crispy_formset_modal.layout import ModalEditFormsetLayout
from crispy_formset_modal.layout import ModalEditLayout
from crispy_forms.layout import Column, Fieldset, Layout, Row, Submit, Field
from crispy_forms.helper import FormHelper
from .models import Reimburse, ReimburseLine



class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, attrs=None):
        super().__init__(attrs)

class ReimburseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field("title"),
                    Field("description")
                ), 
                Column(
                    Field("approver"),
                    Row(Column(Field("start_date")), Column(Field("end_date"))),
                )
            ),
        )
        super(ReimburseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Reimburse
        exclude = ['created_date', 'total', 'state']
        widgets = {
                'user': forms.HiddenInput(),
                "start_date": DateInput(),
                "end_date": DateInput()}

class LineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap5/layout/inline_field.html'
        self.helper.layout = Layout(
            Row(
            Column(Field('item')),
            Column(Field('attachment')),
            Column(Field('quantity')),
            Column(Field('price')),
            )
        )
        super(LineForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = ReimburseLine
        fields = "__all__"
