from django import forms
import datetime
from .models import Plan, Cost


class CreateNewPlan(forms.ModelForm):
    """Form for creating new plan with defined properties"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'] = forms.CharField(label='Title', max_length=200)
        self.fields['total_members'] = forms.IntegerField(
            label='Number of members', min_value=1)
        self.fields['payment_date'] = forms.DateField(label='Payment date',
                                                      required=False, initial=datetime.datetime.now)
        self.fields['plan_info'] = forms.CharField(
            label='Additional informations', required=False)

    class Meta:
        model = Plan
        # exclude it from form
        exclude = ['user']


class CreateNewCost(forms.ModelForm):
    """Form for creating new cost with defined properties"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cost_name'] = forms.CharField(
            label='Name', max_length=200)
        self.fields['cost'] = forms.DecimalField(
            label='Cost', max_digits=50, decimal_places=2, min_value=0.01)
        self.fields['number_of_members'] = forms.IntegerField(
            label='Number of members', min_value=1)
        self.fields['payment_date'] = forms.DateField(label='Payment date',
                                                      required=False, initial=datetime.datetime.now)
        self.fields['cost_info'] = forms.CharField(
            label='Additional informations', required=False)

    class Meta:
        model = Cost
        # exclude it from form
        exclude = ['plan_of_cost', 'cost_status']
