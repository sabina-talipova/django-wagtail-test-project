from django.db import models
from django.urls import reverse
from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField



class Blog(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    content = RichTextField(blank=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("date"),
        FieldPanel("content"),
    ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_detail", args=[str(self.id)])
