from django.core.paginator import Paginator, EmptyPage

def paginate_users(request, users, results):
    page = request.GET.get('page', 1)
    paginator = Paginator(users, results)
    try:
            users = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        users = paginator.page(page)

    left_index = (int(page) - 2)
    if left_index < paginator.num_pages:
        left_index = 1

    right_index = (int(page) + 3)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
        
    custom_range = range(left_index, right_index)

    return custom_range, users