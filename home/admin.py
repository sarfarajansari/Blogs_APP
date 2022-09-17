from django.contrib import admin
from .models import*


class BloggerAdmin(admin.ModelAdmin):
    list_display=("Username","user","title","BP","password")
    filter_horizontal=("article",)

class ArticleAdmin(admin.ModelAdmin):
    list_display=("title","author")
    filter_horizontal=("comments",)

class CommentsAdmin(admin.ModelAdmin):
    list_display=("user","comment")

class UserAdmin(admin.ModelAdmin):
    list_display=("name","email")



# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comments,CommentsAdmin)
admin.site.register(Feedback)
admin.site.register(Paragraphs)
admin.site.register(Username)
admin.site.register(Blogger,BloggerAdmin)
admin.site.register(Theme)
admin.site.register(Gradient)
admin.site.register(fontstyles)
admin.site.register(defaultthemes)