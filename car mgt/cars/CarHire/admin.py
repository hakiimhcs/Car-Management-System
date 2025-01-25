from django.contrib import admin
from .models import Parking,Cars,Reservation,CarTypes
# Register your models here.
admin.site.register(Parking)
admin.site.register(Cars)
admin.site.register(Reservation)
admin.site.register(CarTypes)
admin.site.site_title = "Muntisa Motors Uganda"
admin.site.site_header = "Muntisa Motors Uganda"
admin.site.index_title = "Muntisa Motors Uganda"