from django import forms
from .models import Booking
import datetime

class BookingRequestForm(forms.ModelForm):
    travel_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date', 'min': datetime.date.today().strftime('%Y-%m-%d')})
    )

    class Meta:
        model = Booking
        fields = [
            'guest_name', 'guest_email', 'guest_phone',
            'travel_date', 'adults_count', 'children_count',
            'pickup_location', 'special_requests'
        ]
        widgets = {
            'guest_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'guest_email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}),
            'guest_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number with Country Code'}),
            'adults_count': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 50}),
            'children_count': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 50}),
            'pickup_location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Hotel / Airport / Preferred Pickup Point'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Dietary requirements, room preferences, accessibility requests, etc.'}),
        }

    def clean_travel_date(self):
        date = self.cleaned_data.get('travel_date')
        if date and date < datetime.date.today():
            raise forms.ValidationError("Travel date cannot be in the past.")
        return date
