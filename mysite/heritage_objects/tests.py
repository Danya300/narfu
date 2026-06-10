from django.test import TestCase
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from .models import (
    HeritageObjectPage,
    HeritageObjectIndexPage,
    VideoBlock,
    DocumentBlock,
    ComparisonBlock,
    PanoramaBlock,
)


class HeritageObjectPageTests(WagtailPageTestCase):
    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite",
            root_page=root_page,
            is_default_site=True,
        )
        # Создаём индексную страницу
        self.index_page = HeritageObjectIndexPage(
            title="Объекты наследия",
            intro="Каталог объектов",
        )
        root_page.add_child(instance=self.index_page)

        # Создаём объект наследия
        self.heritage_object = HeritageObjectPage(
            title="Усадьба XVIII века",
            address="г. Архангельск, ул. Набережная, д. 1",
            phone="+7 (8182) 00-00-00",
            description="Историческая усадьба",
            year_built="1780",
            architectural_style="Классицизм",
            latitude=64.5399,
            longitude=40.5153,
            map_link="https://yandex.ru/maps",
        )
        self.index_page.add_child(instance=self.heritage_object)

    def test_heritage_object_can_be_created(self):
        self.assertTrue(
            HeritageObjectPage.objects.filter(title="Усадьба XVIII века").exists()
        )

    def test_heritage_object_is_renderable(self):
        self.assertPageIsRenderable(self.heritage_object)

    def test_heritage_object_template_used(self):
        response = self.client.get(self.heritage_object.url)
        self.assertTemplateUsed(
            response, "heritage_objects/heritage_object_page.html"
        )

    def test_heritage_object_fields(self):
        obj = HeritageObjectPage.objects.get(title="Усадьба XVIII века")
        self.assertEqual(obj.address, "г. Архангельск, ул. Набережная, д. 1")
        self.assertEqual(obj.phone, "+7 (8182) 00-00-00")
        self.assertEqual(obj.description, "Историческая усадьба")
        self.assertEqual(obj.year_built, "1780")
        self.assertEqual(obj.architectural_style, "Классицизм")
        self.assertEqual(obj.latitude, 64.5399)
        self.assertEqual(obj.longitude, 40.5153)
        self.assertEqual(obj.map_link, "https://yandex.ru/maps")

    def test_heritage_object_as_child_of_index(self):
        obj = HeritageObjectPage.objects.get(title="Усадьба XVIII века")
        self.assertEqual(obj.get_parent().pk, self.index_page.pk)


class HeritageObjectIndexPageTests(WagtailPageTestCase):
    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite",
            root_page=root_page,
            is_default_site=True,
        )
        self.index_page = HeritageObjectIndexPage(
            title="Объекты наследия",
            intro="Каталог объектов наследия",
        )
        root_page.add_child(instance=self.index_page)

        self.heritage_object = HeritageObjectPage(
            title="Дом купца",
            address="ул. Ленина, 5",
        )
        self.index_page.add_child(instance=self.heritage_object)

    def test_index_page_is_renderable(self):
        self.assertPageIsRenderable(self.index_page)

    def test_index_page_template_used(self):
        response = self.client.get(self.index_page.url)
        self.assertTemplateUsed(
            response, "heritage_objects/heritage_object_index_page.html"
        )

    def test_index_page_context(self):
        response = self.client.get(self.index_page.url)
        self.assertIn("heritage_objects", response.context)
        objects_in_context = list(response.context["heritage_objects"])
        self.assertIn(self.heritage_object, objects_in_context)

    def test_index_page_intro(self):
        self.assertEqual(self.index_page.intro, "Каталог объектов наследия")


class HeritageObjectBlockTests(TestCase):
    """Тесты для StreamField блоков"""

    def test_video_block_render(self):
        block = VideoBlock()
        value = block.to_python({
            "title": "Тестовое видео",
            "video_embed": "<iframe src='https://example.com/video'></iframe>",
            "description": "<p>Описание видео</p>",
        })
        self.assertEqual(value["title"], "Тестовое видео")
        self.assertIn("example.com", value["video_embed"])
        self.assertIn("Описание видео", value["description"].source)

    def test_document_block_render(self):
        block = DocumentBlock()
        # Проверяем, что блок корректно сериализуется
        value = block.get_default()
        self.assertIsNotNone(value)

    def test_comparison_block_default(self):
        block = ComparisonBlock()
        value = block.get_default()
        self.assertIsNotNone(value)

    def test_panorama_block_default(self):
        block = PanoramaBlock()
        value = block.get_default()
        self.assertIsNotNone(value)


class HeritageObjectPageParentTests(WagtailPageTestCase):
    """Проверка родительских/дочерних типов страниц"""

    def test_heritage_object_can_be_under_index(self):
        self.assertCanCreateAt(
            HeritageObjectIndexPage, HeritageObjectPage
        )

    def test_heritage_object_can_be_under_root(self):
        self.assertCanCreateAt(Page, HeritageObjectPage)
