from locust import HttpUser, task, between
import random


class NarfuUser(HttpUser):
    wait_time = between(1, 5)

    @task(10)
    def home_page(self):
        self.client.get("/")

    @task(5)
    def search_page(self):
        self.client.get("/search/")

    @task(3)
    def admin_login_page(self):
        self.client.get("/admin/")

    @task(2)
    def django_admin_page(self):
        self.client.get("/django-admin/")

    @task(1)
    def random_wagtail_page(self):
        self.client.get("/about/")