from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from wagtail.models import Page
from django.db.models import Q


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    if search_query:
        # Преобразуем запрос в нижний регистр для нечувствительного поиска
        query_lower = search_query.lower()
        
        # Собираем все live страницы и фильтруем вручную по всем данным
        all_live_pages = Page.objects.live().specific()
        
        matched_pages = []
        for p in all_live_pages:
            # Проверяем название страницы
            if query_lower in p.title.lower():
                matched_pages.append(p)
                continue
                
            # Проверяем intro (если есть)
            if hasattr(p, 'intro') and p.intro and query_lower in str(p.intro).lower():
                matched_pages.append(p)
                continue
                
            # Проверяем description (для объектов наследия)
            if hasattr(p, 'description') and p.description and query_lower in p.description.lower():
                matched_pages.append(p)
                continue
                
            # Проверяем address (для объектов наследия)
            if hasattr(p, 'address') and p.address and query_lower in p.address.lower():
                matched_pages.append(p)
                continue
                
            # Проверяем content (StreamField) - преобразуем в строку
            if hasattr(p, 'content') and p.content:
                # Преобразуем StreamValue в строку
                content_str = str(p.content)
                if query_lower in content_str.lower():
                    matched_pages.append(p)
                    continue
            
            # Проверяем year_built
            if hasattr(p, 'year_built') and p.year_built and query_lower in p.year_built.lower():
                matched_pages.append(p)
                continue
                
            # Проверяем architectural_style
            if hasattr(p, 'architectural_style') and p.architectural_style and query_lower in p.architectural_style.lower():
                matched_pages.append(p)
                continue
        
        search_results = matched_pages
    else:
        search_results = []

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )
