from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
path("",views.index, name='index'),
path("user_signup",views.user_signup, name='user_signup'),
path("user_login",views.user_login, name='user_login'),
path("user_logout",views.user_logout, name='user_logout'),
path("user_profile",views.user_profile, name='user_profile'),
path("add_room",views.add_room, name='add_room'),
path("book_room/<int:id>",views.book_room, name='book_room'),
path("user_booking/<int:id>",views.user_booking, name='user_booking'),
path("cancel_reservation/<int:id>",views.cancel_reservation, name='cancel_reservation'),
path("manager_cancel_reservation/<int:id>",views.manager_cancel_reservation, name='manager_cancel_reservation'),
path("delete_room/<int:id>",views.delete_room, name='delete_room'),
path("update_room/<int:id>",views.update_room, name='update_room'),
path("delete_user/<int:id>",views.delete_user, name='delete_user'),
path("view_user/",views.view_user, name='view_user'),
path("view_reservation/",views.view_reservation, name='view_reservation'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
