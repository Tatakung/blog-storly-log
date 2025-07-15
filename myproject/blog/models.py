from django.db import models
from category.models import Category
from django.contrib.auth.models import User
# Create your models here.
class Blog(models.Model):  
    name = models.CharField(max_length=200) 
    discrp = models.CharField(max_length=300, blank=True)  
    content = models.TextField()  # เนื้อหาเต็ม
    views = models.IntegerField(default=0)  # ยอดวิว
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # รูป
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)  # หมวดหมู่
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,related_name='comments')
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"โดย {self.customer} บน {self.blog.name}"