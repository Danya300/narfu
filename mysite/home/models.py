from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.contrib.table_block.blocks import TableBlock


class VideoBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Название видео")
    video_embed = blocks.TextBlock(required=True, help_text="HTML код встраивания видео (iframe)")
    description = blocks.RichTextBlock(required=False, help_text="Описание видео")

    class Meta:
        template = 'home/blocks/video_block.html'
        icon = 'media'
        label = 'Видео'


class VideoFileBlock(blocks.StructBlock):
    """Блок для загрузки видео файла"""
    title = blocks.CharBlock(required=True, help_text="Название видео")
    video_file = DocumentChooserBlock(required=True, help_text="Загрузите видео файл (mp4, webm, mov)")
    description = blocks.RichTextBlock(required=False, help_text="Описание видео")
    poster = ImageChooserBlock(required=False, help_text="Постер (обложка) для видео")

    class Meta:
        template = 'home/blocks/video_file_block.html'
        icon = 'media'
        label = 'Видео файл'


class AudioFileBlock(blocks.StructBlock):
    """Блок для загрузки аудио файла"""
    title = blocks.CharBlock(required=True, help_text="Название аудио")
    audio_file = DocumentChooserBlock(required=True, help_text="Загрузите аудио файл (mp3, wav, ogg)")
    description = blocks.RichTextBlock(required=False, help_text="Описание аудио")

    class Meta:
        template = 'home/blocks/audio_file_block.html'
        icon = 'media'
        label = 'Аудио файл'


class NewsBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Заголовок новости")
    content = blocks.RichTextBlock(required=True, help_text="Текст новости")
    date = blocks.DateBlock(required=True, help_text="Дата публикации")
    image = ImageChooserBlock(required=False, help_text="Изображение новости")

    class Meta:
        template = 'home/blocks/news_block.html'
        icon = 'newspaper'
        label = 'Новость'


class ContactInfoBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Название контакта")
    value = blocks.CharBlock(required=True, help_text="Значение контакта")
    icon = blocks.CharBlock(required=False, help_text="CSS класс иконки")

    class Meta:
        template = 'home/blocks/contact_info_block.html'
        icon = 'address-book'
        label = 'Контактная информация'


class PartnerBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True, help_text="Название партнёра")
    logo = ImageChooserBlock(required=False, help_text="Логотип партнёра")
    description = blocks.RichTextBlock(required=False, help_text="Описание")
    website = blocks.URLBlock(required=False, help_text="Сайт партнёра")

    class Meta:
        template = 'home/blocks/partner_block.html'
        icon = 'user'
        label = 'Партнёр'


class ExpertBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True, help_text="Имя эксперта")
    photo = ImageChooserBlock(required=False, help_text="Фото эксперта")
    position = blocks.CharBlock(required=False, help_text="Должность")
    bio = blocks.RichTextBlock(required=False, help_text="Биография")

    class Meta:
        template = 'home/blocks/expert_block.html'
        icon = 'user'
        label = 'Эксперт'


class HomePage(Page):
    # StreamField для гибкого контента
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title", icon='title')),
        ('paragraph', blocks.RichTextBlock(icon='pilcrow')),
        ('image', ImageChooserBlock(icon='image')),
        ('video', VideoBlock()),
        ('video_file', VideoFileBlock()),
        ('audio_file', AudioFileBlock()),
        ('news', NewsBlock()),
        ('contact_info', ContactInfoBlock()),
    ], use_json_field=True, blank=True)

    # Панели администрирования
    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]

    # Поисковые поля
    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"


class AboutPage(Page):
    """Страница 'О нас'"""
    intro = models.TextField(blank=True, help_text="Вводный текст")
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title", icon='title')),
        ('paragraph', blocks.RichTextBlock(icon='pilcrow')),
        ('image', ImageChooserBlock(icon='image')),
        ('video', VideoBlock()),
        ('video_file', VideoFileBlock()),
        ('audio_file', AudioFileBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('content'),
    ]

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


class PartnersPage(Page):
    """Страница 'Партнёры'"""
    intro = models.TextField(blank=True, help_text="Вводный текст")
    content = StreamField([
        ('partner', PartnerBlock()),
        ('heading', blocks.CharBlock(form_classname="full title", icon='title')),
        ('paragraph', blocks.RichTextBlock(icon='pilcrow')),
        ('image', ImageChooserBlock(icon='image')),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    class Meta:
        verbose_name = "Партнёры"
        verbose_name_plural = "Партнёры"


class ExpertsPage(Page):
    """Страница 'Эксперты'"""
    intro = models.TextField(blank=True, help_text="Вводный текст")
    content = StreamField([
        ('expert', ExpertBlock()),
        ('table', TableBlock()),
        ('heading', blocks.CharBlock(form_classname="full title", icon='title')),
        ('paragraph', blocks.RichTextBlock(icon='pilcrow')),
        ('image', ImageChooserBlock(icon='image')),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('content'),
    ]

    class Meta:
        verbose_name = "Эксперты"
        verbose_name_plural = "Эксперты"


class NewsPage(Page):
    """Страница отдельной новости"""
    date = models.DateField(help_text="Дата публикации")
    intro = models.TextField(blank=True, help_text="Краткое описание")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Изображение для анонса новости'
    )
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title", icon='title')),
        ('paragraph', blocks.RichTextBlock(icon='pilcrow')),
        ('image', ImageChooserBlock(icon='image')),
        ('video', VideoBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('image'),
        FieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('content'),
    ]

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class NewsIndexPage(Page):
    """Страница списка новостей"""
    intro = models.TextField(blank=True, help_text="Вводный текст")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        news_pages = NewsPage.objects.live().descendant_of(self).order_by('-date')
        context['news_pages'] = news_pages
        return context

    class Meta:
        verbose_name = "Новости (индекс)"
        verbose_name_plural = "Новости (индекс)"


class ContactPage(Page):
    """Страница 'Контакты'"""
    address = models.CharField(max_length=300, blank=True, help_text="Адрес")
    phone = models.CharField(max_length=50, blank=True, help_text="Телефон")
    email = models.EmailField(blank=True, help_text="Email")
    map_embed = models.TextField(blank=True, help_text="HTML код карты (iframe)")
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title", icon='title')),
        ('paragraph', blocks.RichTextBlock(icon='pilcrow')),
        ('contact_info', ContactInfoBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('address'),
        FieldPanel('phone'),
        FieldPanel('email'),
        FieldPanel('map_embed'),
        FieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('address'),
        index.SearchField('content'),
    ]

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"


class FooterSettings(models.Model):
    # Информация о нас
    about_title = models.CharField(max_length=200, default="О нас", help_text="Заголовок секции 'О нас'")
    about_content = models.TextField(help_text="Текст описания")
    
    # Контактная информация
    address = models.CharField(max_length=300, help_text="Адрес")
    email = models.EmailField(help_text="Email")
    phone = models.CharField(max_length=50, blank=True, help_text="Телефон")
    
    # Социальные сети
    vk_link = models.URLField(blank=True, help_text="Ссылка на VK")
    youtube_link = models.URLField(blank=True, help_text="Ссылка на YouTube")
    telegram_link = models.URLField(blank=True, help_text="Ссылка на Telegram")
    
    # Контактное лицо
    contact_person = models.CharField(max_length=100, help_text="Контактное лицо")
    contact_position = models.CharField(max_length=100, help_text="Должность контактного лица")

    panels = [
        FieldPanel('about_title'),
        FieldPanel('about_content'),
        FieldPanel('address'),
        FieldPanel('email'),
        FieldPanel('phone'),
        FieldPanel('vk_link'),
        FieldPanel('youtube_link'),
        FieldPanel('telegram_link'),
        FieldPanel('contact_person'),
        FieldPanel('contact_position'),
    ]

    class Meta:
        verbose_name = "Настройки футера"
        verbose_name_plural = "Настройки футера"
