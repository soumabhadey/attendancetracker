from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("", views.attendance, name="attendance"),	
	path("course/<int:id>/", views.course, name="course"),
	path("create-course/", views.create_course, name="create-course"),
	path("course/<int:id>/create-subject/", views.create_subject, name="create-subject"),
	path("delete-course/<int:id>/", views.delete_course, name="delete-course"),
	path("course/<int:id>/delete-subject/<int:subjectId>/", views.delete_subject, name="delete-subject"),
	path("delete-user/", views.delete_user, name="delete-user"),
	path("edit-course/<int:id>/", views.edit_course, name="edit-course"),
	path("course/<int:id>/edit-subject/<int:subjectId>/", views.edit_subject, name="edit-subject"),
	path("edit-user/", views.edit_user, name="edit-user"),
	path("login-user/", views.login_user, name="login-user"),
	path("logout-user/", views.logout_user, name="logout-user"),
	path("register-user/", views.register_user, name="register-user"),
]