# chat/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from chat.models import Account, ChatMessage


class AccountAdmin(UserAdmin):
	list_display = ('username','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('username',)
	readonly_fields=('id', 'date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(ChatMessage)