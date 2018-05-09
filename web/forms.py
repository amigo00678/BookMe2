# -*- coding: utf-8 -*-

from django.core.validators import validate_email
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.forms import formset_factory

from web.models import *


class SaveFileMixin(object):
    def save_slider_files(self, files):
        if files:
            slider = ImageSlider.objects.create()

            for file in files:
                image = SliderImage.objects.create(image=file)
                slider.images.add(image)

            return slider


class AuthForm(AuthenticationForm):

    def clean(self):
        cd = super(AuthForm, self).clean()
        email = cd.get('username', None)
        if email:
            validate_email(email)


class FileEditForm(forms.ModelForm, SaveFileMixin):

    top_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    bottom_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = File
        fields = ['name', 'type', 'owner', 'features', 'top_content', 'middle_content', 'bottom_content']

        widgets = {
            'top_content': forms.Textarea(attrs={'class': 'tinymce'}),
            'middle_content': forms.Textarea(attrs={'class': 'tinymce'}),
            'bottom_content': forms.Textarea(attrs={'class': 'tinymce'}),
        }

    def save(self, commit=True):
        instance = super(FileEditForm, self).save(commit=commit)

        if self.files:
            instance.top_slider = self.save_slider_files(self.files.getlist('top_images'))
            instance.bottom_slider = self.save_slider_files(self.files.getlist('bottom_images'))
            instance.save()

        return instance


class UserEditForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['is_active', 'first_name', 'last_name', 'type', 'email']


class UserAddForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['is_active', 'email', 'first_name', 'last_name', 'type']


class FeatureEditForm(forms.ModelForm):

    class Meta:
        model = Feature
        fields = ['name', 'is_main', 'image']

        widgets = {
            'image': forms.FileInput(),
        }


class RoomFeatureEditForm(forms.ModelForm):

    class Meta:
        model = RoomFeature
        fields = ['name', 'image']

        widgets = {
            'image': forms.FileInput(),
        }


class FEReviewEditForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['heading', 'rate', 'pros', 'cons']

        widgets = {
            'heading': forms.Textarea(attrs={'class': 'tinymce'}),
            'pros': forms.Textarea(attrs={'class': 'tinymce'}),
            'cons': forms.Textarea(attrs={'class': 'tinymce'}),
        }


class ReviewEditForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['heading', 'rate', 'pros', 'cons', 'user', 'item']

        widgets = {
            'heading': forms.Textarea(attrs={'class': 'tinymce'}),
            'pros': forms.Textarea(attrs={'class': 'tinymce'}),
            'cons': forms.Textarea(attrs={'class': 'tinymce'}),
        }


class RoomPriceForm(forms.ModelForm):
    class Meta:
        model = RoomPrice
        fields = ['price', 'people_number']


class RoomEditForm(forms.ModelForm):

    room_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Room
        fields = ['name', 'prices', 'users_count', 'count', 'features', 'room_images', 'rest_places']

        widgets = {
            'name': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super(RoomEditForm, self).__init__(*args, **kwargs)
        self.fields['prices'].queryset = RoomPrice.objects.filter(room__id=self.instance.id)
        self.prices_formset = formset_factory(RoomPriceForm, extra=2)

    def clean(self, *args, **kwargs):
        cd = super(RoomEditForm, self).clean(*args, **kwargs)
        pf = self.prices_formset(self.data)
        pf.is_valid()
        return cd

    def save(self, commit=True):
        instance = super(RoomEditForm, self).save(commit=commit)

        if self.files:
            instance.images.all().delete()
            for file in self.files.getlist('room_images'):
                image = SliderImage.objects.create(image=file)
                instance.images.add(image)

        pf = self.prices_formset(self.data)

        for form in pf:
            prices_instance = form.save()
            if prices_instance.price and prices_instance.people_number:
                instance.prices.add(prices_instance)
            else:
                prices_instance.delete()

        return instance


class OrderEditForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['item', 'room', 'user', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(OrderEditForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = settings.DATE_INPUT_FORMATS
        self.fields['end_date'].input_formats = settings.DATE_INPUT_FORMATS


class RestPlacesEditForm(forms.ModelForm):

    class Meta:
        model = RestPlace
        fields = ['name', 'image', 'count']

        widgets = {
            'name': forms.TextInput(),
        }
