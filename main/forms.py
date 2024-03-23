from django import forms

class FishForm(forms.Form):
    photo = forms.ImageField(label='넙치 사진')
    length = forms.FloatField(label='체장(cm)')
    weight = forms.FloatField(label='체중(g)')
    feed_amount = forms.FloatField(label='먹이량(g)')