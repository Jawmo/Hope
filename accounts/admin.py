from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Rooms, Players, Items, Orgs, Npcs, News, Wiki

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'uuid_id', 'char_name', 'date_joined', 'last_login']
    fieldsets = (
        (('User'), {'fields': ('username', 'email','uuid_id', 'char_name', 'date_joined', 'last_login')}),
    )

# class Rooms(CustomUserAdmin):
#     ordering = ['name']
#     list_display = ['name']

admin.site.register(CustomUser, 
					CustomUserAdmin)
admin.site.register(Players)
admin.site.register(Rooms)
admin.site.register(Items)
admin.site.register(Orgs)
admin.site.register(Npcs)
admin.site.register(News)
admin.site.register(Wiki)