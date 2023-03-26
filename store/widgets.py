from django.forms.widgets import ClearableFileInput
from django.utils.html import format_html


class ImagePreviewWidget(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and hasattr(value, "url"):
            img_html = format_html(
                '<br><img src="{}" width="250px" height="auto"/>', value.url)
            html = html + img_html
        return html
