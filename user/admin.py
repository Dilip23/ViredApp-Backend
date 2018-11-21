from django.contrib import admin
from .models import (MediaDB,
                     Request,
                     Profile,
                     Likes,
                     Friends,
                     )
# Register your models here.
admin.site.register(MediaDB)
admin.site.register(Request)
admin.site.register(Profile)
admin.site.register(Likes)
admin.site.register(Friends)
