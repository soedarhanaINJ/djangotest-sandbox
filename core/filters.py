from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

COMPLETE_FILTER = [DjangoFilterBackend, SearchFilter, OrderingFilter]
NO_ORDER_FILTER = [DjangoFilterBackend, SearchFilter]
