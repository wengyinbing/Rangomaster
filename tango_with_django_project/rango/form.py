from django import forms
from rango.models import Category,Page,UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,help_text="Please enter the category name")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(),required=False)

    #嵌套的类，为表单提供额外信息
    class Meta:
        #把这个modelform与一个模型连接起来
        model = Category
        #只有一个元素的元组要加逗号
        fields = ('name',)



class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    class Meta:
        model = Page

        #想在这个表单中添加哪些字段，当然也可以排除一些字段
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data

        url = cleaned_data.get('url')
        # 如果 url 字段不为空，而且不以“http://”开头
        # 在前面加上“http://”
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website','picture')
