# -*- coding: utf-8 -*-

from django.core.validators import validate_email
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from web.models import *


class SaveFileMixin(object):
    def save_files(self, files):
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
        fields = ['name', 'type', 'features', 'top_content', 'middle_content', 'bottom_content']

        widgets = {
            'top_content': forms.Textarea(attrs={'class': 'tinymce'}),
            'middle_content': forms.Textarea(attrs={'class': 'tinymce'}),
            'bottom_content': forms.Textarea(attrs={'class': 'tinymce'}),
        }

    def save(self, commit=True):
        instance = super(FileEditForm, self).save(commit=commit)

        if self.files:
            instance.top_slider = self.save_files(self.files.getlist('top_images'))
            instance.bottom_slider = self.save_files(self.files.getlist('bottom_images'))
            instance.save()

        return instance


class FeatureEditForm(forms.ModelForm):

    class Meta:
        model = Feature
        fields = ['name', 'is_main', 'image']

        widgets = {
            'image': forms.FileInput(),
        }


class ReviewEditForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['heading', 'pros', 'cons']

        widgets = {
            'heading': forms.Textarea(attrs={'class': 'tinymce'}),
            'pros': forms.Textarea(attrs={'class': 'tinymce'}),
            'cons': forms.Textarea(attrs={'class': 'tinymce'}),
        }
