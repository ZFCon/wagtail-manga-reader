from django.db import models
from django.db.models import Q

# Create your models here.
from django.db import models
from .validator import max_value

from modelcluster.fields import ParentalKey
from django.contrib.contenttypes.models import ContentType
from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from taggit.models import TaggedItemBase

from wagtail.core.fields import RichTextField

from save.models import Saved

# Manga Tags 
class MangaPageGenre(TaggedItemBase):
    content_object = ParentalKey(
        'MangaPage',
        related_name='genre_items',
        on_delete=models.CASCADE,
    )

# start Manga page
class MangaPage(Page):
    cover = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    genre = ClusterTaggableManager(through=MangaPageGenre)
    artist = models.CharField(max_length= 30, blank=True)
    rating = models.DecimalField(decimal_places=1, max_digits=3, validators=[max_value])
    description = RichTextField(features= ['bold', 'link'])

    content_panels = Page.content_panels + [
        ImageChooserPanel('cover'),
        MultiFieldPanel([
        FieldPanel('genre'),
        FieldPanel('artist'),
        FieldPanel('rating'),
        FieldPanel('description')
        ], 'About'),
    ]
    def get_context(self, request, *args, **kwargs):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request, *args, **kwargs)

        # save items
        do_save = None
        content_type = ContentType.objects.get_for_model(self.__class__)
        item_saved = Saved.objects.filter(content_type=content_type, item_id=self.id).exists()
        if request.user.is_authenticated:
            if request.GET.get('save', None) != None:
                save = int(request.GET.get('save'))
                if save == 1:
                    do_save = True
                elif save == 0:
                    do_save = False
                    
                # to save item
                if item_saved and do_save:
                    pass
                elif not item_saved and do_save:
                    Saved.objects.create(content_type=content_type, item_id=self.id, user=request.user)
                # to unsave item
                if not item_saved and not do_save:
                    pass
                elif item_saved and not do_save:
                    Saved.objects.filter(content_type=content_type, item_id=self.id, user=request.user).delete()
            
            # context saved
            context['item_saved'] = item_saved
            
        # get related fields
        related = MangaPage.objects.filter(genre__name__in = [i.name for i in self.genre.all()])
        context['related'] = list(set(related))[:4]
        
        return context
    
    parent_page_types = ['home.HomePage']
    subpage_types = ['MangaChaPage']


# start Manga Chapter page

class MangaChaPage(Page):
    cover = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    chapter = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_context(self, request, *args, **kwargs):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request, *args, **kwargs)
        # get parent query
        manga = self.get_ancestors().last
        context['manga'] = manga

        # get related fields
        related = MangaPage.objects.filter(genre__name__in = ['how', 'nice'])
        context['related'] = list(set(related))[:4]
        
        return context

    content_panels = Page.content_panels + [
        ImageChooserPanel('cover'),
        DocumentChooserPanel('chapter'),
    ]
    parent_page_types = ['MangaPage']
    subpage_types = []

    