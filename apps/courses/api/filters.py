from django_filters import Filter, FilterSet, filters
from ..models import *
from rest_framework import filters as r_filters
from transliterate import translit
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity


class FullTextSearchFilterBackend(r_filters.SearchFilter):

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        for search_term in search_terms:
            search_terms = ' '.join(search_terms)
            search_terms = translit(search_terms, 'ru')
            if queryset.filter(name__istartswith=search_terms).count() > 0:
                queryset = queryset.filter(Q(name__istartswith=search_terms),)

            if queryset.filter(name__contains=search_terms).count() > 0:
                queryset = queryset.filter(Q(name__contains=search_terms), )

            else:
                queryset = queryset.annotate(similarity=TrigramSimilarity('name', search_terms), ).filter(
                    Q(name__icontains=search_term) | Q(teachers__name__icontains=search_term) |
                    Q(description__icontains=search_term) | Q(similarity__gt=0.16)
                ).order_by('-similarity')

            return queryset


