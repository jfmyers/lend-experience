# Summary: DocumentForm handles the upload of user files(for now this is intended for only a user's profile picture).
from django import forms

class DocumentForm(forms.Form):
    file = forms.FileField()