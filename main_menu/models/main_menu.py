from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet


@register_snippet
class MainMenu(ClusterableModel):
    MENU_CHOICES = [
        ("header", "Header"),
        ("footer", "Footer"),
    ]

    title = models.CharField(max_length=255)
    menu_type = models.CharField(
        max_length=20,
        choices=MENU_CHOICES,
        default="header",
        help_text="Header / Footer"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("menu_type"),
        InlinePanel("menu_items", label="Menu Items"),
    ]

    def __str__(self):
        return f"{self.get_menu_type_display()} — {self.title}"
