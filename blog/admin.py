from django.contrib import admin
# from . import models
from . models import *

# Register your models here.


# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('email')
#     fields = ['email']
#     search_fields = ['name','email']
#     ordering = ['name']
#     list_filter = ['active','created_on']
#     date_hierarchy = 'created_on'


class PostAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['title']}),
                 (None, {'fields': ['author']}),
                 (None, {'fields': ['category']}),
                 (None, {'fields': ['content']}),
                 ('Tags', {'fields': ['tags'], 'classes': ['collapse']}),
                 (None, {'fields': ['slug']})]
    list_display = ('title', 'author', 'category',)
    search_fields = ['title', 'content']
    ordering = ['-pub_date']
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    filter_horizontal = ('tags',)
    raw_id_fields = ('tags',)
    # prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('slug',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject','date',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Feedback,FeedbackAdmin)

