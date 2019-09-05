from django import forms
from .models import Article
from ckeditor_uploader.widgets import CKEditorUploadingWidget
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude =['author','views','slug','pub_date','create_date','mod_date','users_like']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
           # 'body': forms.Textarea(attrs={'class':'form-control'}),
            'body':CKEditorUploadingWidget(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'}),
            'category': forms.SelectMultiple(attrs={'class':'form-control selectpicker', 'data-live-search':'True'}),
            'tags':forms.SelectMultiple(attrs={'class':'form-control selectpicker', 'data-live-search':'True'})
        }