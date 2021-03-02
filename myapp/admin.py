from django.contrib import admin
from myapp.models import RandomPosts

# Register your models here.
class RandomPostsAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','title','body')

admin.site.register(RandomPosts,RandomPostsAdmin)    