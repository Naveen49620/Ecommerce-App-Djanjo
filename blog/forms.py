from django import forms  # ✅ lowercase 'forms'

class ContactForm(forms.Form):  # ✅ Uppercase 'ContactForm', capital 'F' in Form
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email', required=False)
    message = forms.CharField(label='Message', widget=forms.Textarea)


