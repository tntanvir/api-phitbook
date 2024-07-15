from django.contrib import admin
from .models import Post,Comment,Likes
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['fistname','title','discription','publication_date']

    def fistname(self,obj):
        return obj.user.first_name

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['fistname','post','comment','comment_date']
    def fistname(self,obj):
        return obj.user.first_name
    def post(self,obj):
        return obj.post.title
    


admin.site.register(Likes)
    

admin.site.register(Comment,CommentAdmin)