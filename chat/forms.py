from django.forms import ModelForm

from chat.models import Chat


class NewMessageForm(ModelForm):
    class Meta:
        model = Chat
        fields = ['message']
