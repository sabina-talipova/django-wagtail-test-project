from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock

class HomePage(Page):
    subtitle = models.CharField(max_length=255, blank=True, help_text="Subtitle")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image",
    )

    blocks = StreamField(
        [
            (
                "text_block",
                StructBlock([
                    ("title", CharBlock(required=True, max_length=100)),
                    ("text", RichTextBlock(required=False)),
                ]),
            ),
            (
                "image_block",
                StructBlock([
                    ("image", ImageChooserBlock(required=True)),
                    ("caption", CharBlock(required=False, max_length=250)),
                ]),
            ),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("image"),
        FieldPanel("blocks"),
    ]

    template = "core/home_page/home_page.html"

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
