from django import forms
from .models import Server
from .aes4  import enc,dec

class ServerForm(forms.ModelForm):
    keytext = forms.CharField(max_length=100,required=True,label='Your Key',
                        widget=forms.PasswordInput(attrs={'class': 'form-control', 'onchange': 'checkpass();'}))
    config_text = forms.CharField(max_length=100000, required=False, label='Config Text',
                        widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Server
        fields = ['server_name', 'username', 'password', 'description']
        widgets = {
            'server_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),            
        }

        '''
        def save(self):
            instance = super().save(commit=False)
            encpass = enc(self.cleaned_data['password'],self.cleaned_data['keytext'])
            instance.password = encpass
            instance.save()
            return instance
        '''
