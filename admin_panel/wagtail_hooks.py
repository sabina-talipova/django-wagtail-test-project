from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.images.models import Image
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from core.models.blog import Blog

class BlogViewSet(ModelViewSet):
    model = Blog
    menu_label = "Blogs"
    menu_icon = "doc-full"
    add_to_admin_menu = True
    list_display = ("title", "date")
    search_fields = ("title",)


@hooks.register("register_admin_viewset")
def register_article_viewset():
    return BlogViewSet("blogs")
