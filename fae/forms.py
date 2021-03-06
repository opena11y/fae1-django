from django import forms
from django.contrib.auth.models import User
from models import UserProfile, UserReport

class TextFieldWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs',{}).update({'size': '60', 'class': 'textfield', 'onfocus': 'this.select()'})
        super(TextFieldWidget, self).__init__(*args, **kwargs)

class BasicEvalForm(forms.Form):
    url = forms.URLField(label='URL:', initial='http://', verify_exists=True, widget=TextFieldWidget)
    dhtml = forms.BooleanField(label='Include DHTML content', initial=0, widget=forms.CheckboxInput, required=False)

class DepthEvalForm(forms.Form):
    DEPTH_CHOICES = (
        (0, 'Top-level page only'),
        (1, 'Include second-level pages'),
        (2, 'Include third-level pages'),
    )

    SPAN_CHOICES = (
        (0, 'Specified domain only'),
        (1, 'Next-level subdomains'),
    )

    url = forms.URLField(label='URL:', initial='http://', verify_exists=True, widget=TextFieldWidget)
    title = forms.CharField(label='Report Title:', max_length=128, required=False, widget=TextFieldWidget)
    depth = forms.ChoiceField(label='Depth of Evaluation', choices=DEPTH_CHOICES, initial=0, widget=forms.RadioSelect)
    span = forms.ChoiceField(label='Follow Links in', choices=SPAN_CHOICES, initial=0, widget=forms.RadioSelect, required=False)
    dhtml = forms.BooleanField(label='Include DHTML content', initial=0, widget=forms.CheckboxInput, required=False)

class MultiEvalForm(forms.Form):
    TEXTAREA_ATTRS = { 'rows': '10', 'cols': '60', 'class': 'textfield', 'onfocus': 'this.select()' }
    urls = forms.CharField(label='URLs:', widget=forms.Textarea(attrs=TEXTAREA_ATTRS))
    title = forms.CharField(label='Report Title:', max_length=128, required=False, widget=TextFieldWidget)
    dhtml = forms.BooleanField(label='Include DHTML content', initial=0, widget=forms.CheckboxInput, required=False)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('org',)

class ManageReportForm(forms.ModelForm):
    class Meta:
        model = UserReport
        fields = ('archive',)
