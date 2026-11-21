from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate(objects, request, per_page=10):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    page.elided_page_range = paginator.get_elided_page_range(page.number)
    return page
