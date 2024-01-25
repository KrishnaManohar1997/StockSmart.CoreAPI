def get_limited_paginated_results(request, queryset, paginator, max_limit=10):
    limit = int(paginator.get_limit(request))
    MAX_FEED_LIMIT = max_limit
    if limit > MAX_FEED_LIMIT:
        paginated_queryset = queryset[:MAX_FEED_LIMIT]
    else:
        paginated_queryset = queryset[:limit]
    return paginator.paginate_queryset(paginated_queryset, request)
