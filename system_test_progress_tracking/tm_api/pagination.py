from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomListPageSizePagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'current_site': self.request.get_host(),
            'page_size': self.get_page_size(self.request),
            'count': self.page.paginator.count,
            'page_number': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'has_previous': self.page.has_previous(),
            "previous_page_number": self.page.previous_page_number() if self.page.has_previous() else None,
            'has_next': self.page.has_next(),
            "next_page_number": self.page.next_page_number() if self.page.has_next() else None,
            'results': data
        })
