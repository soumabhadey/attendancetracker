from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Course(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name
	
	def attendance(self):
		# avg_attendance = self.subject_set.aggregate(avg_attendance=Avg('present') * 100 / (Avg('present') + Avg('absent')))['avg_attendance']

		# return avg_attendance

		total_present = self.subject_set.aggregate(total_present=Sum('present'))['total_present']
		total_absent = self.subject_set.aggregate(total_absent=Sum('absent'))['total_absent']

		if total_present is None:
			total_present = 0
		if total_absent is None:
			total_absent = 0

		total_classes = total_present + total_absent
		if total_classes == 0:
			return 100
		else:
			return (total_present * 100) / total_classes


class Subject(models.Model):
	name = models.CharField(max_length=100)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	present = models.IntegerField()
	absent = models.IntegerField()

	def __str__(self):
		return self.name

	def attendance(self):
		total = self.present + self.absent
		percent = self.present * 100 / total
		
		return percent