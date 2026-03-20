from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class CustomLimitOffsetPagination(LimitOffsetPagination):
     def get_paginated_response(self, data):
        return Response({
            'count': len(data),              # current page size
            'total': self.count,            # total records
            'results': data
        })