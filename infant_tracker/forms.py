from django import forms

class ContactForm(forms.Form):
    created_at = forms.DateTimeField(widget=forms.DateTimeInput)
    event_type = forms.CharField()
    event_notes = forms.CharField(widget=forms.Textarea)

    def submit_form(self):
        pass
