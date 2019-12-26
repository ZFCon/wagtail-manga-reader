from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

from manga.models import MangaChaPage, MangaPage


# slider image
# Manga gallery
class SliderPageImage(Orderable):
    page = ParentalKey('HomePage', related_name="slider_image")
    slider_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        ImageChooserPanel("slider_image"),
        ]

class HomePage(Page):
    parent_page_types = ['wagtailcore.Page']

    # active home page item
    active_slider = models.BooleanField(default=False)
    active_full_manga_lastest = models.BooleanField(default=False)
    active_lastest = models.BooleanField(default=True)

    content_panels = Page.content_panels + [
        FieldPanel('active_slider'),
        MultiFieldPanel([InlinePanel('slider_image', max_num=5)], 'Add image to slider'),
        FieldPanel('active_full_manga_lastest'),
        FieldPanel('active_lastest'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # manga
        full_manga = MangaPage.objects.live().public().order_by('-first_published_at')
        context['full_manga'] = full_manga

        # posts
        posts = MangaChaPage.objects.live().public().order_by('-first_published_at')
        context['posts'] = posts
        return context
