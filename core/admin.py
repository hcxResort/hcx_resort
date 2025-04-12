from django.contrib import admin
from .models import (
    UserProfile, RoomType, Room, ServiceType, Service,
    Reservation, ReservationService, Payment, Review
)

admin.site.register(UserProfile)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Reservation)
admin.site.register(ReservationService)
admin.site.register(Payment)
admin.site.register(Review)
