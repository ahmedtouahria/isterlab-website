from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, 
        on_delete=models.CASCADE, related_name='subcategories'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Inquiry(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="inquiries")
    user_message = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry about {self.category.name}"
