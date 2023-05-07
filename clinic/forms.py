from django import forms
from clinic.models import Review
from django.utils.translation import gettext_lazy as _


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["doctor", "patient", "text"]
        widgets = {
            "doctor": forms.HiddenInput(),
            "patient": forms.HiddenInput(),
            "text": forms.Textarea(attrs={"class": "review-textarea",
                                          "id": "review-text",
                                          "name": "review_text",
                                          "placeholder": _("Введіть текст відгуку...")})
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields["text"].label = "Текст відгуку"
