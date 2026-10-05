from django.contrib import admin
from poll.models import CustomUser,POll,Choices
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(POll)
admin.site.register(Choices)