from django import forms
from .models import CustomEnquiry
import datetime

class CustomEnquiryForm(forms.ModelForm):
    preferred_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date', 'min': datetime.date.today().strftime('%Y-%m-%d')})
    )

    class Meta:
        model = CustomEnquiry
        fields = [
            'name', 'email', 'phone', 'destination_preference',
            'preferred_date', 'duration_days', 'travelers_count',
            'budget_range', 'preferences', 'message'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'destination_preference': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Destination (e.g., Swiss Alps, Maldives, Japan)'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 60, 'placeholder': 'Days'}),
            'travelers_count': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 50, 'placeholder': 'Travelers'}),
            'budget_range': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Budget Range (e.g. $2,000 - $5,000)'}),
            'preferences': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Luxury resorts, Honeymoon, Private villa, Family activities'}),
            'message': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Tell us your dream vacation requirements...'}),
        }
