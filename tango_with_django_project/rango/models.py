from django.db import models
from django.template.defaultfilters import  slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128,unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        print(self.slug)
        super(Category, self).save(*args, **kwargs)

    class Meta():
        #防止数据库admin管理界面的拼写错误 不然显示的是Category
        verbose_name_plural = 'Categories'

    def __str__(self):#python2 还要加上__unicode__
        return self.name


class Page(models.Model):
    #需要两个参数 外键 和删除方式
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    #建立与User的关系,里面需要提供一个删除的的方式on_delete
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    #添加自己想加的属性
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images',blank=True)

    #覆盖__str__()方法，返回有意义的字符串
    def __str__(self):
        return self.user.username

