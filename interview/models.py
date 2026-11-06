from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLES = [('student', 'Student'), ('evaluator', 'Evaluator'), ('admin', 'Admin')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default='student')


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes/')
    education = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Interview(models.Model):
    LEVELS = [('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')]
    STATUS = [('in_progress', 'In Progress'), ('completed', 'Completed')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    difficulty_level = models.CharField(max_length=10, choices=LEVELS)
    status = models.CharField(max_length=15, choices=STATUS, default='in_progress')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)


class Question(models.Model):
    TYPES = [('resume_based', 'Resume Based'), ('follow_up', 'Follow Up')]
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=15, choices=TYPES)
    order_no = models.IntegerField()
    asked_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    transcript_text = models.TextField()
    response_time_sec = models.FloatField(default=0)
    answered_at = models.DateTimeField(auto_now_add=True)


class Evaluation(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    correctness_marks = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    technical_marks = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    communication_marks = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    grammar_pronunciation_marks = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    clarity_marks = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    response_time_marks = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    feedback = models.TextField(blank=True)
    evaluated_at = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    interview = models.OneToOneField(Interview, on_delete=models.CASCADE)
    overall_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    improvement_areas = models.TextField(blank=True)
    report_pdf = models.FileField(upload_to='reports/', blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)