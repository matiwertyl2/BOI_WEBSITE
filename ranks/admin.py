from django.contrib import admin
from .models import Ranking


class RankingAdmin(admin.ModelAdmin):
    list_display = ['olympiad', 'ranking']
    ordering = ['olympiad']


admin.site.register(Ranking, RankingAdmin)
