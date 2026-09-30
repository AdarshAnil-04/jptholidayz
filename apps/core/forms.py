from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your Email Address'}))
    phone = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Phone Number'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 5, 'placeholder': 'How can we help plan your holiday?'}))
