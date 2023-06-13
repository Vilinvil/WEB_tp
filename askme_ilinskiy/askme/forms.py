from . import models

from django import forms
from django.contrib.auth.models import User

MIN_LENGTH_PASSWORD = 3


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=MIN_LENGTH_PASSWORD, widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(min_length=MIN_LENGTH_PASSWORD, widget=forms.PasswordInput)
    password_check = forms.CharField(min_length=MIN_LENGTH_PASSWORD, widget=forms.PasswordInput)

    class Meta:
        model = models.MyUser
        fields = ["username", "email", "password", "password_check", 'avatar']

    def clean(self):
        password = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')
        if password_check != password:
            raise forms.ValidationError("Password doesn't match")

        return self.cleaned_data

    def clean_username(self):
        print(self.cleaned_data.get('username'))
        print(models.MyUser.objects.filter(profile__username=self.cleaned_data.get('username')).exists())
        if models.MyUser.objects.filter(profile__username=self.cleaned_data.get('username')).exists():
            raise forms.ValidationError("User with same username exist")

        return self.cleaned_data.get("username")

    def clean_email(self):
        if models.MyUser.objects.filter(profile__email=self.cleaned_data.get('email')).exists():
            raise forms.ValidationError("User with same email exist")

        return self.cleaned_data.get("email")

    def save(self):
        profile = User.objects.create_user(username=self.cleaned_data.get('username'),
                                           email=self.cleaned_data.get('email'),
                                           password=self.cleaned_data.get('password'))
        return models.MyUser.objects.create(profile=profile, avatar=self.cleaned_data.get('avatar'))


class NewPostForm(forms.ModelForm):
    tag1 = forms.CharField(max_length=31, required=False)
    tag2 = forms.CharField(max_length=31, required=False)
    tag3 = forms.CharField(max_length=31, required=False)

    class Meta:
        model = models.Post
        fields = ["title", 'text']

    def clean(self):
        tag1 = self.cleaned_data.get('tag1')
        tag2 = self.cleaned_data.get('tag2')
        tag3 = self.cleaned_data.get('tag3')
        print(tag1)
        print(tag2)
        print(tag3)
        if (tag1 == tag2 and tag1 != "") or (tag1 == tag3 and tag1 != "") or (tag2 == tag3 and tag3 != ""):
            raise forms.ValidationError("Don`t use same tags")

        return self.cleaned_data

    def save(self, username):
        print(username)
        user = models.MyUser.objects.get(profile__username=username)
        post = models.Post.objects.create(title=self.cleaned_data.get('title'), text=self.cleaned_data.get('text'),
                                          user_id=user)

        tags = []
        tag1 = self.cleaned_data['tag1']
        if tag1:
            tag, created = models.Tag.objects.get_or_create(name=tag1.strip())
            tag.post.set([post])
            if created:
                tags.append(tag)

        tag2 = self.cleaned_data['tag2']
        if tag2:
            tag, created = models.Tag.objects.get_or_create(name=tag2.strip())
            tag.post.set([post])
            if created:
                tags.append(tag)

        tag3 = self.cleaned_data['tag3']
        if tag3:
            tag, created = models.Tag.objects.get_or_create(name=tag3.strip())
            tag.post.set([post])
            if created:
                tags.append(tag)

        post.save()
        return post


class NewAnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ["text"]

    def save(self, username, post_id):
        print(username)
        user = models.MyUser.objects.get(profile__username=username)
        post = models.Post.objects.get(pk=post_id)
        answer = models.Answer.objects.create(text=self.cleaned_data.get('text'),
                                              user_id=user, post_id=post)

        answer.save()
        return answer


class SettingsForm(forms.ModelForm):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    avatar = forms.ImageField(required=False)
    username_request = None
    email_request = None

    class Meta:
        model = models.MyUser
        fields = ["username", "email", 'avatar']


    def clean_username(self):
        print("undo" + self.username_request.__str__())
        if models.MyUser.objects.filter(profile__username=self.cleaned_data.get(
                'username')).exists() and self.cleaned_data.get('username').__str__() != self.username_request.__str__():
            raise forms.ValidationError("User with same username exist")

        print("after" + self.username_request.__str__())
        return self.cleaned_data.get("username")

    def clean_email(self):
        if models.MyUser.objects.filter(
                profile__email=self.cleaned_data.get('email')).exists() and self.email_request.__str__() != self.cleaned_data.get('email').__str__():
            raise forms.ValidationError("User with same email exist")

        return self.cleaned_data.get("email")

    def save(self, username):
        print("in save" + username.__str__())
        user = models.MyUser.objects.get(profile__username=username)
        user.profile.username = self.cleaned_data.get('username')
        user.profile.email = self.cleaned_data.get('email')
        user.profile.password = self.cleaned_data.get('password')
        print(self.cleaned_data.get('avatar'))
        if self.cleaned_data.get('avatar') is not None:
            user.avatar = self.cleaned_data.get('avatar')
        user.save()
        return user
