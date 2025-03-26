from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()  # Date of Birth
    nrc = models.CharField(max_length=50, unique=True)  # National Registration Card number (assuming it's unique)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)  # Phone number
    address = models.TextField()  # Long address details
    grade = models.CharField(max_length=10)  # Grade (A, B, etc.)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name  # This will display the student's name in the admin panel

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Subject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField()
    subject1_marks = models.FloatField()
    subject2_marks = models.FloatField()
    subject3_marks = models.FloatField()
    subject4_marks = models.FloatField()
    subject5_marks = models.FloatField()
    subject6_marks = models.FloatField()

    @property
    def total_marks(self):
        return self.subject1_marks + self.subject2_marks + self.subject3_marks + self.subject4_marks + self.subject5_marks + self.subject6_marks
    
    def __str__(self):
        return f"{self.student.name} - Year: {self.year} - Total Marks: {self.total_marks}"
