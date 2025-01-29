# forms.py
from django import forms
from .models import RiskAssessment, Asset, Vulnerability, Threat, Risk
from django.core.validators import MinValueValidator, MaxValueValidator

class RiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = ['title', 'description', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")
        return cleaned_data

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'value', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'value': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }

    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value and value < 0:
            raise forms.ValidationError("Asset value cannot be negative.")
        return value

class VulnerabilityForm(forms.ModelForm):
    class Meta:
        model = Vulnerability
        fields = ['name', 'description', 'asset', 'severity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'severity': forms.NumberInput(attrs={
                'min': '1',
                'max': '10',
                'class': 'range-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asset'].queryset = Asset.objects.order_by('name')
        self.fields['severity'].help_text = "Rate from 1 (lowest) to 10 (highest)"

class ThreatForm(forms.ModelForm):
    THREAT_TYPES = [
        ('external', 'External'),
        ('internal', 'Internal'),
        ('natural', 'Natural'),
        ('human', 'Human'),
        ('technical', 'Technical'),
    ]

    threat_type = forms.ChoiceField(choices=THREAT_TYPES)

    class Meta:
        model = Threat
        fields = ['name', 'description', 'threat_type', 'likelihood']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'likelihood': forms.NumberInput(attrs={
                'min': '1',
                'max': '10',
                'class': 'range-input'
            }),
        }

    def clean_likelihood(self):
        likelihood = self.cleaned_data.get('likelihood')
        if likelihood < 1 or likelihood > 10:
            raise forms.ValidationError("Likelihood must be between 1 and 10.")
        return likelihood

class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ['name', 'description', 'asset', 'vulnerability', 'threat', 
                 'likelihood', 'impact', 'status', 'mitigation_plan']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'likelihood': forms.NumberInput(attrs={
                'min': '1',
                'max': '10',
                'class': 'range-input'
            }),
            'impact': forms.NumberInput(attrs={
                'min': '1',
                'max': '10',
                'class': 'range-input'
            }),
            'mitigation_plan': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asset'].queryset = Asset.objects.order_by('name')
        self.fields['vulnerability'].queryset = Vulnerability.objects.order_by('name')
        self.fields['threat'].queryset = Threat.objects.order_by('name')

        # Add help text for scoring fields
        self.fields['likelihood'].help_text = "Rate from 1 (lowest) to 10 (highest)"
        self.fields['impact'].help_text = "Rate from 1 (lowest) to 10 (highest)"

    def clean(self):
        cleaned_data = super().clean()
        likelihood = cleaned_data.get('likelihood')
        impact = cleaned_data.get('impact')

        if likelihood and impact:
            if likelihood < 1 or likelihood > 10:
                raise forms.ValidationError("Likelihood must be between 1 and 10.")
            if impact < 1 or impact > 10:
                raise forms.ValidationError("Impact must be between 1 and 10.")

        # Ensure the vulnerability is associated with the selected asset
        asset = cleaned_data.get('asset')
        vulnerability = cleaned_data.get('vulnerability')
        if asset and vulnerability and vulnerability.asset != asset:
            raise forms.ValidationError(
                "The selected vulnerability must be associated with the selected asset."
            )

        return cleaned_data

class RiskResponseForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ['status', 'mitigation_plan']
        widgets = {
            'mitigation_plan': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_mitigation_plan(self):
        status = self.cleaned_data.get('status')
        mitigation_plan = self.cleaned_data.get('mitigation_plan')
        
        if status == 'mitigated' and not mitigation_plan:
            raise forms.ValidationError(
                "A mitigation plan is required when status is set to 'mitigated'."
            )
        return mitigation_plan
    
class ImpactForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ['impact']