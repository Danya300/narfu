from django.test import TestCase
from wagtail.images.models import Image
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from .models import (
    AboutPage,
    AudioFileBlock,
    ContactInfoBlock,
    ContactPage,
    ExpertBlock,
    ExpertsPage,
    FooterSettings,
    HomePage,
    NewsBlock,
    NewsIndexPage,
    NewsPage,
    PartnerBlock,
    PartnersPage,
    VideoBlock,
    VideoFileBlock,
)


class HomeSetUpTests(WagtailPageTestCase):
    """
    Tests for basic page structure setup and HomePage creation.
    """

    def test_root_create(self):
        root_page = Page.objects.get(pk=1)
        self.assertIsNotNone(root_page)

    def test_homepage_create(self):
        root_page = Page.objects.get(pk=1)
        homepage = HomePage(title="Home")
        root_page.add_child(instance=homepage)
        self.assertTrue(HomePage.objects.filter(title="Home").exists())


class HomeTests(WagtailPageTestCase):
    """
    Tests for homepage functionality and rendering.
    """

    def setUp(self):
        """
        Create a homepage instance for testing.
        """
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite",
            root_page=root_page,
            is_default_site=True,
        )
        self.homepage = HomePage(title="Home")
        root_page.add_child(instance=self.homepage)

    def test_homepage_is_renderable(self):
        self.assertPageIsRenderable(self.homepage)

    def test_homepage_template_used(self):
        response = self.client.get(self.homepage.url)
        self.assertTemplateUsed(response, "home/home_page.html")

    def test_homepage_content_streamfield_default(self):
        """Проверяем, что StreamField content пустой при создании"""
        self.assertEqual(list(self.homepage.content), [])


class HomePageBlockTests(TestCase):
    """Тесты для StreamField блоков HomePage"""

    def test_video_block(self):
        block = VideoBlock()
        value = block.to_python({
            "title": "Промо-ролик",
            "video_embed": "<iframe src='https://youtube.com/embed/test'></iframe>",
            "description": "<p>Описание промо</p>",
        })
        self.assertEqual(value["title"], "Промо-ролик")
        self.assertIn("youtube.com", value["video_embed"])
        self.assertIn("Описание промо", value["description"].source)

    def test_video_file_block_default(self):
        block = VideoFileBlock()
        value = block.get_default()
        self.assertIsNotNone(value)

    def test_audio_file_block_default(self):
        block = AudioFileBlock()
        value = block.get_default()
        self.assertIsNotNone(value)

    def test_news_block(self):
        block = NewsBlock()
        value = block.to_python({
            "title": "Новость дня",
            "content": "<p>Текст новости</p>",
            "date": "2026-06-10",
        })
        self.assertEqual(value["title"], "Новость дня")
        self.assertEqual(value["date"].isoformat(), "2026-06-10")

    def test_contact_info_block(self):
        block = ContactInfoBlock()
        value = block.to_python({
            "title": "Телефон",
            "value": "+7 (8182) 00-00-00",
            "icon": "fa-phone",
        })
        self.assertEqual(value["title"], "Телефон")
        self.assertEqual(value["value"], "+7 (8182) 00-00-00")
        self.assertEqual(value["icon"], "fa-phone")

    def test_partner_block_default(self):
        block = PartnerBlock()
        value = block.get_default()
        self.assertIsNotNone(value)

    def test_expert_block_default(self):
        block = ExpertBlock()
        value = block.get_default()
        self.assertIsNotNone(value)


class AboutPageTests(WagtailPageTestCase):
    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite",
            root_page=root_page,
            is_default_site=True,
        )
        self.about_page = AboutPage(
            title="О нас",
            intro="Вводный текст о компании",
        )
        root_page.add_child(instance=self.about_page)

    def test_about_page_is_renderable(self):
        self.assertPageIsRenderable(self.about_page)

    def test_about_page_template_used(self):
        response = self.client.get(self.about_page.url)
        self.assertTemplateUsed(response, "home/about_page.html")

    def test_about_page_intro(self):
        self.assertEqual(self.about_page.intro, "Вводный текст о компании")


class PartnersPageTests(WagtailPageTestCase):
    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite",
            root_page=root_page,
            is_default_site=True,
        )
        self.partners_page = PartnersPage(
            title="Партнёры",
            intro="Наши партнёры",
        )
        root_page.add_child(instance=self.partners_page)

    def test_partners_page_is_renderable(self):
        self.assertPageIsRenderable(self.partners_page)

    def test_partners_page_template_used(self):
        response = self.client.get(self.partners_page.url)
        self.assertTemplateUsed(response, "home/partners_page.html")


class ExpertsPageTests(WagtailPageTestCase):
    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite",
            root_page=root_page,
            is_default_site=True,
        )
        self.experts_page = ExpertsPage(
            title="Эксперты",
            intro="Наши эксперты",
        )
        root_page.add_child(instance=self.experts_page)

    def test_experts_page_is_renderable(self):
        self.assertPageIsRenderable(self.experts_page)

    def test_experts_page_template_used(self):
        response = self.client.get(self.experts_page.url)
        self.assertTemplateUsed(response, "home/experts_page.html")


class NewsPageTests(WagtailPageTestCase):
    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite",
            root_page=root_page,
            is_default_site=True,
        )
        from datetime import date
        self.news_page = NewsPage(
            title="Новость 1",
            date=date(2026, 6, 10),
            intro="Краткое описание",
        )
        root_page.add_child(instance=self.news_page)

    def test_news_page_is_renderable(self):
        self.assertPageIsRenderable(self.news_page)

    def test_news_page_template_used(self):
        response = self.client.get(self.news_page.url)
        self.assertTemplateUsed(response, "home/news_page.html")

    def test_news_page_date(self):
        np = NewsPage.objects.get(title="Новость 1")
        self.assertEqual(np.date.isoformat(), "2026-06-10")


class NewsIndexPageTests(WagtailPageTestCase):
    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite",
            root_page=root_page,
            is_default_site=True,
        )
        from datetime import date

        self.news_index = NewsIndexPage(
            title="Новости",
            intro="Список новостей",
        )
        root_page.add_child(instance=self.news_index)

        self.news1 = NewsPage(
            title="Новость А",
            date=date(2026, 6, 10),
        )
        self.news_index.add_child(instance=self.news1)

        self.news2 = NewsPage(
            title="Новость Б",
            date=date(2026, 6, 5),
        )
        self.news_index.add_child(instance=self.news2)

    def test_news_index_is_renderable(self):
        self.assertPageIsRenderable(self.news_index)

    def test_news_index_context(self):
        response = self.client.get(self.news_index.url)
        self.assertIn("news_pages", response.context)
        news_in_context = list(response.context["news_pages"])
        self.assertIn(self.news1, news_in_context)
        self.assertIn(self.news2, news_in_context)

    def test_news_order(self):
        """Новости должны быть отсортированы по дате DESC"""
        response = self.client.get(self.news_index.url)
        news_in_context = list(response.context["news_pages"])
        self.assertEqual(news_in_context[0], self.news1)  # 2026-06-10
        self.assertEqual(news_in_context[1], self.news2)  # 2026-06-05


class ContactPageTests(WagtailPageTestCase):
    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite",
            root_page=root_page,
            is_default_site=True,
        )
        self.contact_page = ContactPage(
            title="Контакты",
            address="г. Архангельск, ул. Набережная, д. 1",
            phone="+7 (8182) 00-00-00",
            email="info@example.com",
            map_embed="<iframe src='https://maps.example.com'></iframe>",
        )
        root_page.add_child(instance=self.contact_page)

    def test_contact_page_is_renderable(self):
        self.assertPageIsRenderable(self.contact_page)

    def test_contact_page_template_used(self):
        response = self.client.get(self.contact_page.url)
        self.assertTemplateUsed(response, "home/contact_page.html")

    def test_contact_page_fields(self):
        cp = ContactPage.objects.get(title="Контакты")
        self.assertEqual(cp.address, "г. Архангельск, ул. Набережная, д. 1")
        self.assertEqual(cp.phone, "+7 (8182) 00-00-00")
        self.assertEqual(cp.email, "info@example.com")
        self.assertIn("maps.example.com", cp.map_embed)


class FooterSettingsTests(TestCase):
    def test_footer_settings_defaults(self):
        fs = FooterSettings(
            about_content="Текст о нас",
            address="г. Архангельск",
            email="info@example.com",
            phone="+7 (8182) 00-00-00",
            contact_person="Иванов И.И.",
            contact_position="Директор",
        )
        self.assertEqual(fs.about_title, "О нас")
        self.assertEqual(fs.about_content, "Текст о нас")
        self.assertEqual(fs.address, "г. Архангельск")
        self.assertEqual(fs.email, "info@example.com")
        self.assertEqual(fs.phone, "+7 (8182) 00-00-00")
        self.assertEqual(fs.contact_person, "Иванов И.И.")
        self.assertEqual(fs.contact_position, "Директор")
        # Социальные сети по умолчанию пустые
        self.assertEqual(fs.vk_link, "")
        self.assertEqual(fs.youtube_link, "")
        self.assertEqual(fs.telegram_link, "")