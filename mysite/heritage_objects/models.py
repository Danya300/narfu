from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index


class VideoBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Название видео")
    video_embed = blocks.RawHTMLBlock(required=True, help_text="HTML код встраивания видео (iframe)")
    description = blocks.RichTextBlock(required=False, help_text="Описание видео")

    class Meta:
        template = 'heritage_objects/blocks/video_block.html'
        icon = 'media'
        label = 'Видео'


class DocumentBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Название документа")
    document = DocumentChooserBlock(required=True, help_text="PDF документ")
    description = blocks.RichTextBlock(required=False, help_text="Описание документа")

    class Meta:
        template = 'heritage_objects/blocks/document_block.html'
        icon = 'doc-full'
        label = 'Документ'


class ComparisonBlock(blocks.StructBlock):
    """Слайдер сравнения до/после"""
    before_image = ImageChooserBlock(required=True, help_text="Изображение до (до реставрации)")
    after_image = ImageChooserBlock(required=True, help_text="Изображение после (после реставрации)")
    caption = blocks.CharBlock(required=False, help_text="Подпись")

    class Meta:
        template = 'heritage_objects/blocks/comparison_block.html'
        icon = 'arrows-left-right'
        label = 'Сравнение до/после'


class PanoramaBlock(blocks.StructBlock):
    """Блок с 360° панорамой (Pannellum)"""
    title = blocks.CharBlock(required=False, help_text="Название панорамы (необязательно)")
    panorama = ImageChooserBlock(required=True, help_text="Файл панорамы 360° (изображение JPG/PNG из галереи)")
    description = blocks.RichTextBlock(required=False, help_text="Описание панорамы (необязательно)")

    class Meta:
        template = 'heritage_objects/blocks/panorama_block.html'
        icon = 'image'
        label = '360° Панорама'


class HeritageObjectPage(Page):
    # Основная информация
    address = models.CharField(max_length=200, verbose_name="Адрес")
    phone = models.CharField(max_length=50, verbose_name="Телефон", blank=True)
    description = models.TextField(verbose_name="Описание объекта", blank=True)
    year_built = models.CharField(max_length=50, verbose_name="Год постройки", blank=True)
    architectural_style = models.CharField(max_length=100, verbose_name="Архитектурный стиль", blank=True)

    # Координаты для карты
    latitude = models.FloatField(verbose_name="Широта", blank=True, null=True)
    longitude = models.FloatField(verbose_name="Долгота", blank=True, null=True)
    map_link = models.URLField(verbose_name="Ссылка на карту", blank=True, help_text="Ссылка на Яндекс.Карты или другую карту")

    # Галерея изображений
    gallery = StreamField([
        ('image', ImageChooserBlock(icon='image', help_text='Изображение для галереи')),
    ], use_json_field=True, blank=True, help_text="Галерея изображений")

    # StreamField для медиаконтента
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title", icon='title')),
        ('paragraph', blocks.RichTextBlock(icon='pilcrow')),
        ('image', ImageChooserBlock(icon='image')),
        ('video', VideoBlock()),
        ('document', DocumentBlock()),
        ('comparison', ComparisonBlock()),
        ('panorama', PanoramaBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('address'),
        FieldPanel('phone'),
        FieldPanel('description'),
        FieldPanel('year_built'),
        FieldPanel('architectural_style'),
        FieldPanel('latitude'),
        FieldPanel('longitude'),
        FieldPanel('map_link'),
        FieldPanel('gallery'),
        FieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('address'),
        index.SearchField('description'),
        index.SearchField('year_built'),
        index.SearchField('architectural_style'),
    ]

    class Meta:
        verbose_name = "Объект историко-архитектурного наследия"
        verbose_name_plural = "Объекты историко-архитектурного наследия"


class HeritageObjectIndexPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        heritage_objects = HeritageObjectPage.objects.live().child_of(self)
        context['heritage_objects'] = heritage_objects
        return context
