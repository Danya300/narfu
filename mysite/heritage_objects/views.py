from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import HeritageObjectPage, HeritageObjectIndexPage


def heritage_object_list(request):
    """Список объектов наследия"""
    index_page = HeritageObjectIndexPage.objects.first()
    if not index_page:
        return HttpResponse("Страница с объектами наследия не найдена")
    
    context = index_page.get_context(request)
    return render(request, 'heritage_objects/heritage_object_index_page.html', context)


def heritage_object_detail(request, pk):
    """Детальная страница объекта наследия"""
    heritage_object = get_object_or_404(HeritageObjectPage, pk=pk, live=True)
    return render(request, 'heritage_objects/heritage_object_page.html', {
        'page': heritage_object
    })