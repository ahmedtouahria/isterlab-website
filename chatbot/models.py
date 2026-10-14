from django.db import models
from landing.models import Blog



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    message = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, 
        on_delete=models.CASCADE, related_name='subcategories'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Response(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="responses")
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    blogs = models.ManyToManyField(Blog, related_name="blogs", blank=True)
    def __str__(self):
        return self.response
    
