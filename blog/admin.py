from django.contrib import admin

from models import Category, Entry

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'posted'
    filter_horizontal = ('categories',)
    list_display = ('title', 'posted', 'last_updated')
    list_filter = ('author', 'categories')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')

admin.site.register(Category)
admin.site.register(Entry, EntryAdmin)
