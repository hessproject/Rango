from django.contrib import admin
from rango.models import Category, Page
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    fields = ["name", "slug", "views", "likes"]
    list_display = ["name", "slug", "views", "likes",]
    prepopulated_fields = {"slug":('name',)}

class PageAdmin(admin.ModelAdmin):
    fields = ["title", "category", "url"]
    list_display = ["title", "category", "url",]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)

