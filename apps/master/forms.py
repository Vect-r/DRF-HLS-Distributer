from django.contrib.admin.helpers import ActionForm
from django import forms
from .models import Quality

class HLSActionForm(ActionForm):
    pref_quality = forms.ChoiceField(
        choices=Quality.QUALITY_CHOICES,
        required=False,
        label="Quality",
        initial="1440p"
    )

    pref_codec = forms.ChoiceField(
        choices=Quality.CODECS,
        required=False,
        label="Codec",
        initial="h264"
    )