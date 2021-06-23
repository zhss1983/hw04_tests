from django.contrib import admin

from .models import Group, Post

EMPTY = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title', 'slug')
    empty_value_display = EMPTY


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = EMPTY


admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
