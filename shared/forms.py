from django import forms


class SearchForm(forms.Form):
  query = forms.CharField(label='بحث', widget=forms.TextInput(attrs={'placeholder': 'ابحث هنا...'}))