from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import University, Course, Degree, Review, Enrollment, StudentProfile, Location
from django.utils import timezone
from .forms import StudentRegistrationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

#testing the string representations of various models in a university system
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


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)

    #tests whether the login page is displayed correctly by checking that the HTTP status code is 200
    def test_get_login_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    #tests whether a user can log in with valid credentials by posting a username 
    # and password to the login page and checking that they are redirected to the university list page
    def test_login_with_valid_credentials(self):
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('universities:university_list'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    #tests whether a user is not able to log in with invalid credentials by posting 
    # a username and wrong password to the login page and checking that the HTTP status 
    # code is 200, that the login.html template is used, and that the response contains an error message
    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.url, {'username': self.username, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Please enter a correct username and password.')

    #tests whether a user is not able to log in with missing credentials by posting a username 
    # to the login page and checking that the HTTP status code is 200, that the login.html template 
    # is used, and that the response contains an error messag
    def test_login_with_missing_credentials(self):
        response = self.client.post(self.url, {'username': self.username})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'This field is required.')



class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass',
            'password2': 'testpass',
            'date_of_birth': timezone.now().date(),
        }
    #verifies that the register view returns a valid
    # response when accessed with GET, that the correct 
    # template is used, and that a StudentRegistrationForm instance is used in the context.
    def test_register_view_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertIsInstance(response.context['form'], StudentRegistrationForm)

    #simulates an invalid form submission (in this case, with an invalid email format) 
    # and checks that the response is a status code of 200, that the correct template is used,
    #  that a StudentRegistrationForm instance is used in the context, and that an error message is displayed.
    def test_register_view_POST_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid_email'  # invalid email format
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertIsInstance(response.context['form'], StudentRegistrationForm)

        
    
    
        
    
