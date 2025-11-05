from wagtail import blocks
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock

class CustomImageBlock(StructBlock):
    template = "core/blocks/custom_image_block.html"
    title = CharBlock(required=True, max_length=100, help_text="Title")
    text = RichTextBlock(required=False, help_text="Content")
    image = ImageChooserBlock(required=True, help_text="Image")

    class Meta:
        icon = "edit"
        label = "Custom Image Block"
