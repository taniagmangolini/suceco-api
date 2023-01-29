"""Custom Pagination Class"""

from rest_framework import pagination


class CustomLimitOffsetPagination(pagination.LimitOffsetPagination):
    """The limit_query_param and offset_query_param are the query params
    to be used for limit and offset.
    Default_limit if no query parameter is provided.
    Max_limit to restrict the max number of rows returned in a page.
    The offset means the starting point of the page in relation
    to the result-set."""
    default_limit = 20
    limit_query_param = 'l'
    offset_query_param = 'o'
    max_limit = 20
