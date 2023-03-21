from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import University, Course, Degree, Review, Enrollment, StudentProfile, Location

class ModelsTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Test Location", longitude=1.0, latitude=2.0)
        self.degree = Degree.objects.create(name="Test Degree", description="Test Description")
        self.university = University.objects.create(name="Test University", location=self.location, logo="test.png", description="Test Description", website="http://test.com", contact_email="test@test.com")
        self.course = Course.objects.create(name="Test Course", course_code="TC101", description="Test Description", university=self.university)
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.review = Review.objects.create(user=self.user, university=self.university, course=self.course, value_for_money=4, teaching_quality=4, course_content=4, job_prospects=4, review_text="Test Review")

    def test_location_str(self):
        self.assertEqual(str(self.location), "Test Location")

    def test_degree_str(self):
        self.assertEqual(str(self.degree), "Test Degree")

    def test_university_str(self):
        self.assertEqual(str(self.university), "Test University")

    def test_course_str(self):
        self.assertEqual(str(self.course), "TC101: Test Course")

    def test_enrollment_str(self):
        enrollment = Enrollment.objects.create(user=self.user, university=self.university, degree=self.degree)
        enrollment.courses.set([self.course])
        self.assertEqual(str(enrollment), "testuser - Test University (Test Degree)")



        
    
    
        
    
