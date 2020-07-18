from django.contrib import admin
from favorite.models import Favorite,Favorite_link_with_contact
# Register your models here.
admin.site.register(Favorite)
admin.site.register(Favorite_link_with_contact)
