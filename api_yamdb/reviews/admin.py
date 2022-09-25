from django.contrib import admin
from users.models import User

from .models import Category, Comments, Genres, Review, Title

admin.site.register(Category)
admin.site.register(Genres)
admin.site.register(Review)
admin.site.register(Comments)
admin.site.register(Title)
admin.site.register(User)
