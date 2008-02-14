from django import newforms as forms

class TextFieldWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs',{}).update({'size': '60', 'class': 'textfield', 'onfocus': 'this.select()'})
        super(TextFieldWidget, self).__init__(*args, **kwargs)

class BasicEvalForm(forms.Form):
    url = forms.URLField(label='URL:', initial='http://', verify_exists=True, widget=TextFieldWidget)
    title = forms.CharField(label='Report Title:', max_length=128, required=False, widget=TextFieldWidget)

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

class MultiEvalForm(forms.Form):
    TEXTAREA_ATTRS = { 'rows': '10', 'cols': '60', 'class': 'textfield', 'onfocus': 'this.select()' }
    urls = forms.CharField(label='URLs:', widget=forms.Textarea(attrs=TEXTAREA_ATTRS))
    titles = forms.CharField(label='Report Title:', max_length=128, required=False, widget=TextFieldWidget)
