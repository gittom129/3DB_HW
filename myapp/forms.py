from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError("Only CSV files are allowed.")
        return file
