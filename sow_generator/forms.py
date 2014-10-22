from django import forms

from sow_generator.models import Repository


class GenerateForm(forms.Form):
    document_key = forms.CharField(widget=forms.widgets.HiddenInput)
    repos = forms.CharField(widget=forms.widgets.HiddenInput)

    def __init__(self, *args, **kwargs):
        document_key = kwargs.pop("document_key")
        allowed_repos = kwargs.pop("allowed_repos")
        super(GenerateForm, self).__init__(*args, **kwargs)
        self.fields["document_key"].initial = document_key
        self.fields["repos"].initial \
            = ",".join([str(o.id) for o in allowed_repos])

    def clean_repos(self):
        data = self.cleaned_data["repos"]
        result = []
        for id in data.split(","):
            result.append(Repository.objects.get(id=id))
        return result
