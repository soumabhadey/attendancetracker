from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CourseForm, SubjectForm
from .models import Course, Subject

@login_required(login_url="login-user")
def attendance(request):
	context = {}
	if request.user.is_authenticated:
		courses = Course.objects.filter(user=request.user)
		for course in courses:
			course.attendancepercent = format(course.attendance(), ".2f")

		context = {
			"courses": courses,
		}
	return render(request, "attendance/attendance.html", context)


@login_required(login_url="login-user")
def course(request, id):
	context = {
		"id": id,
	}
	if request.user.is_authenticated:
		if request.method == "POST":
			subject_id = request.POST.get("subject_id")
			status = request.POST.get("status")
			subject = get_object_or_404(Subject, pk=subject_id)
			if status == "Present":
				subject.present += 1
			elif status == "Absent":
				subject.absent += 1
			
			subject.save()
			return redirect("course", id)

		course = get_object_or_404(Course, pk=id)
		subjects = Subject.objects.filter(course=course)
		for subject in subjects:
			subject.attendancepercent = format(subject.attendance(), ".2f")


		context["subjects"] = subjects
	return render(request, "attendance/course.html", context)


@login_required(login_url="login-user")
def create_course(request):
	form = CourseForm
	if request.method == "POST":
		form = CourseForm(request.POST)
		if form.is_valid():
			course = form.save(commit=False)
			course.user = request.user
			course.save()
			return redirect("attendance")
	
	context = {
		"form": form,
	}
	return render(request, "attendance/create-course.html", context)


@login_required(login_url="login-user")
def create_subject(request, id):
	form = SubjectForm
	if request.method == "POST":
		form = SubjectForm(request.POST)
		if form.is_valid():
			subject = form.save(commit=False)
			course = Course.objects.get(id=id)
			subject.course = course
			subject.save()
			return redirect("course", id)
		
	context = {
		"form": form,
	}
	return render(request, "attendance/create-subject.html", context)


@login_required(login_url="login-user")
def delete_course(request, id):
	course = Course.objects.get(id=id)
	if request.method == "POST":
		course.delete()
		return redirect("attendance")
	
	context = {
		"obj": course,
	}

	return render(request, "attendance/delete.html", context)


@login_required(login_url="login-user")
def delete_subject(request, id, subjectId):
	subject = Subject.objects.get(id=subjectId)
	if request.method == "POST":
		subject.delete()
		return redirect("course", id=id)
	context = {
		"obj": subject,
	}
	return render(request, "attendance/delete.html", context)


@login_required(login_url="login-user")
def delete_user(request):
	user = request.user
	if request.method == "POST":
		user.delete()
		return redirect("home")
	
	context = {
		"obj": user.username,
	}
	return render(request, "attendance/delete.html", context)


@login_required(login_url="login-user")
def edit_course(request, id):
	course = Course.objects.get(id=id)
	form = CourseForm(instance=course)

	if request.method == "POST":
		form = CourseForm(request.POST, instance=course)
		if form.is_valid():
			form.save()
			return redirect("attendance")
	
	context = {
		"form": form,
	}
	return render(request, "attendance/edit-course.html", context)


@login_required(login_url="login-user")
def edit_subject(request, id, subjectId):
	subject = Subject.objects.get(id=subjectId)
	form = SubjectForm(instance=subject)

	if request.method == "POST":
		form = SubjectForm(request.POST, instance=subject)
		if form.is_valid():
			form.save()
			return redirect("course", id=id)
		
	context = {
		"form": form,
	}

	return render(request, "attendance/edit-subject.html", context)


@login_required(login_url="login-user")
def edit_user(request):
	user = request.user
	form = UserCreationForm(instance=user)
	if request.method == "POST":
		form = UserCreationForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
			return redirect("attendance")
		else:
			messages.error(request, "Invalid credentials")

	context = {
		"form": form,
	}
	return render(request, "attendance/edit-user.html", context)


def login_user(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		try:
			user = User.objects.get(username=username)
		except:
			messages.error(request, "User not found")

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect("attendance")
		else:
			messages.error(request, "Invalid credentials")

	context = {}
	return render(request, "attendance/login-user.html", context)

@login_required(login_url="login-user")
def logout_user(request):
	logout(request)
	return redirect("home")


def register_user(request):
	form = UserCreationForm
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			login(request, user)
			return redirect("attendance")
		else:
			messages.error(request, "Invalid credentials")
		
	context = {
		"form": form,
	}
	return render(request, "attendance/register-user.html", context)