from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

class MenuItem(models.Model):
    menu = ParentalKey(
        "main_menu.MainMenu",
        on_delete=models.CASCADE,
        related_name="menu_items",
    )
    title = models.CharField(max_length=255)
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Page Link",
    )
    link_url = models.URLField(
        blank=True,
        verbose_name="External URL",
    )
    sort_order = models.IntegerField(default=0)

    panels = [
        FieldPanel("title"),
        PageChooserPanel("link_page"),
        FieldPanel("link_url"),
    ]

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.title

    @property
    def url(self):
        if self.link_page:
            return self.link_page.url
        return self.link_url
