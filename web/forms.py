# -*- coding: utf-8 -*-

from django.core.validators import validate_email
from django import forms
from django.contrib.auth.forms import AuthenticationForm

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


class RoomEditForm(forms.ModelForm):

    room_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Room
        fields = ['name', 'price', 'users_count', 'count', 'features', 'room_images']

        widgets = {
            'name': forms.TextInput(),
        }

    def save(self, commit=True):
        instance = super(RoomEditForm, self).save(commit=commit)

        if self.files:
            instance.images.all().delete()
            for file in self.files.getlist('room_images'):
                image = SliderImage.objects.create(image=file)
                instance.images.add(image)

        return instance
