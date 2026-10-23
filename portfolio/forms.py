from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Hidden from people; bots tend to fill it in.
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "tabindex": "-1", "autocomplete": "off",
    }))

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "reason", "message"]
        labels = {
            "name": "Your name",
            "email": "Email",
            "reason": "What it's about",
            "message": "Message",
        }
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "reason": forms.RadioSelect,
            "message": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "The role or project, timeline, and anything I should read first.",
            }),
        }
        error_messages = {
            "name": {"required": "Add your name so I know who to reply to."},
            "email": {
                "required": "Add an email address so I can reply.",
                "invalid": "This email address looks incomplete. Check for a missing @ or domain.",
            },
            "message": {"required": "Write a short message. A couple of lines is enough."},
        }

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("This message is very short. Add a line about the role or project.")
        return message

    def is_spam(self):
        return bool(self.cleaned_data.get("website"))
