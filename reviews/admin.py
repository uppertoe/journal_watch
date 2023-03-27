from django.contrib import admin

from .models import Journal, Article, Review, Issue, Comment

# Register your models here.

class SaveAuthorMixin:
    '''Overrides save_model to set author field to request.user'''
    def save_model(self, request, obj, form, change):
        if obj.author is None:
            obj.author = request.user
        super().save_model(request, obj, form, change)


class JournalAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'abbreviation')


class ArticleAdmin(SaveAuthorMixin, admin.ModelAdmin):
    list_display = ('name', 'journal', 'year')
    search_fields = ('name', 'journal')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('article', 'author')
    list_filter = ('author',)
    search_fields = ('article',)
    readonly_fields = ('slug', 'author')

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('accounts.change_author'):
            fields = list(self.readonly_fields).remove('author')
            return fields
        return super.get_readonly_fields(self, request, obj)


class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ('name', 'reviews')
    readonly_fields = ('slug',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author')
    list_filter = ('author',)
    search_fields = ('article',)
    readonly_fields = ('author',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('accounts.change_author'):
            fields = list(self.readonly_fields).remove('author')
            return fields
        return super.get_readonly_fields(self, request, obj)

admin.site.register(Journal, JournalAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
