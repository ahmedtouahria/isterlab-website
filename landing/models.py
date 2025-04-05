import uuid
from django.db import models
from ckeditor.fields import RichTextField

from django.template.defaultfilters import slugify

class Project(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    content = RichTextField()
    video = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='project_principal_images/')
    date = models.DateTimeField(null=True, blank=True)
    client = models.CharField(max_length=255, null=True, blank=True)
    technologies = models.CharField(max_length=255, null=True, blank=True)
    live = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

class ProjectImage(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')
    created_at = models.DateTimeField(auto_now=True)

class Testimonial(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)

    name = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    image = models.ImageField(upload_to='client_images/')
    content = models.TextField()
    rate = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)


class Service(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)

    name = models.CharField(max_length=255)
    short_description = models.TextField()
    content = RichTextField()
    icon = models.ImageField(upload_to='service_icons/')
    image = models.ImageField(upload_to='service_images/')
    video = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=300,blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)

        super(Service, self).save(*args, **kwargs) # Call the real save() method

class ServiceFAQ(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE,related_name="faqs")
    question = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

class Solution(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=255)
    short_description = models.TextField()
    content = RichTextField()
    icon = models.ImageField(upload_to='service_icons/')
    image = models.ImageField(upload_to='service_images/')
    video = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=300,blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super(Solution, self).save(*args, **kwargs) # Call the real save() method

class SolutionFAQ(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    service = models.ForeignKey(Solution, on_delete=models.CASCADE,related_name="faqs")
    question = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


class Coverage(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()

class FAQ(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    question = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


class Brand(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    logo = models.ImageField(upload_to="brands",)
    name = models.CharField(max_length=150)


class Contact(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class ContactPartner(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    company_url = models.CharField(max_length=255,blank=True, null=True)

    email = models.EmailField(max_length=255)
    subject = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class NewslaterSubscriber(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Blog(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = RichTextField()
    image = models.ImageField(upload_to="blogs", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.TextField()
    author = models.CharField(max_length=150,blank=True, null=True)
    slug = models.CharField(max_length=300,blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs) # Call the real save() method