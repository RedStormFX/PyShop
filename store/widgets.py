from django.forms.widgets import ClearableFileInput
from django.utils.html import format_html
from store.models import Product


class ImagePreviewWidget(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and hasattr(value, "url"):
            product = Product()
            product.image = value
            img_html = format_html(
                '<br><img src="{}" width="250px" height="auto"/>', product.get_image_url())
            html = html + img_html
        return html
