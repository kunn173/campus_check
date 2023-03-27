from django.shortcuts import render, redirect, get_object_or_404
from .models import University, Course, Location, Review, Enrollment, StudentProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import ReviewForm, StudentProfileForm, StudentRegistrationForm
from django.db.models import Avg, Sum, Q
import json
from django.contrib import messages
from django.views.generic import ListView #XuanmingFeng
from django.http import JsonResponse


def search_suggestions(request):
    #search term is extracted from the GET parameters of the request
    search_term = request.GET.get('term', '')
    #universities, courses, and cities that match the search term are queried
    universities = University.objects.filter(Q(name__icontains=search_term) | 
                                              Q(location__name__icontains=search_term))
    courses = Course.objects.filter(name__icontains=search_term)
    cities = University.objects.filter(location__name__icontains=search_term).values_list('location__name', flat=True)
    suggestions = {
        'universities': list(universities.values_list('name', flat=True)),
        'courses': list(courses.values_list('name', flat=True)),
        'cities': list(set(cities)),
    }
    return JsonResponse(suggestions)

@login_required
def student_profile(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        profile = StudentProfile(user=request.user)
        profile.save()

    # Get the Enrollment object for the current user
    enrollment = Enrollment.objects.filter(user=request.user).first()

    # Get the courses related to the Enrollment object, if it exists
    if enrollment:
        courses = enrollment.courses.all()
    else:
        courses = Course.objects.none()

    reviews = Review.objects.filter(user=request.user)
    ratings_by_course = {}

    for review in reviews:
        if review.course_id not in ratings_by_course:
            ratings_by_course[review.course_id] = {
                'value_for_money': [review.value_for_money],
                'teaching_quality': [review.teaching_quality],
                'course_content': [review.course_content],
                'job_prospects': [review.job_prospects],
                'review_text': [review.review_text],
            }
        else:
            ratings_by_course[review.course_id]['value_for_money'].append(review.value_for_money)
            ratings_by_course[review.course_id]['teaching_quality'].append(review.teaching_quality)
            ratings_by_course[review.course_id]['course_content'].append(review.course_content)
            ratings_by_course[review.course_id]['job_prospects'].append(review.job_prospects)
            ratings_by_course[review.course_id]['review_text'].append(review.review_text)

    for course in courses:
        if course.id in ratings_by_course:
            course.avg_rating = sum(ratings_by_course[course.id]['value_for_money'][:3]) / (4 * len(ratings_by_course[course.id]['value_for_money'][:3]))
            course.review_text = ratings_by_course[course.id]['review_text'][0]
        else:
            course.avg_rating = None
            course.review_text = None

    form = StudentProfileForm(instance=profile)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been updated successfully.')
            return redirect(reverse('student_profile'))

    context = {
        'form': form,
        'courses': courses
    }

    return render(request, 'campus/student_profile.html', context)


@login_required
def submit_review(request, course_name_slug):
    course = get_object_or_404(Course, slug=course_name_slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user, course=course)
        if form.is_valid():
            enrollment = Enrollment.objects.filter(user=request.user, courses=course).first()
            #Check if the user has enrolled in the course, if not, return an error message and redirect the user to the course_detail page.
            if not enrollment:
                messages.error(request, "You cannot review a course that you have not enrolled in.")
                return redirect('universities:course_detail', course_name_slug=course_name_slug)
            #Check if the user has already submitted a review for this course, if yes, return an error message and redirect the user to the course_detail page
            if Review.objects.filter(user=request.user, course=course).exists():
                messages.error(request, "You have already submitted a review for this course.")
                return redirect('universities:course_detail', course_name_slug=course_name_slug)
            review = form.save(commit=False)
            review.user = request.user
            review.course = course
            review.university = course.university
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('universities:course_detail', course_name_slug=course_name_slug)
    else:
        form = ReviewForm(user=request.user, course=course)
    return render(request, 'campus/submit_review.html', {'form': form, 'course': course})


def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('universities:university_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'campus/index.html')


def university_list(request):
    universities = University.objects.all()
    search_term = request.GET.get('search', '')
    # Filter universities based on search term 
    if search_term:
        universities = universities.filter(Q(name__icontains=search_term) | 
                                           Q(location__name__icontains=search_term) | 
                                           Q(degree__name__icontains=search_term) | 
                                           Q(courses__name__icontains=search_term))

    university_ratings = {}
    # Loop through universities, prefetch courses and reviews, and calculate ratings
    for university in universities.select_related('location').prefetch_related('courses__review_set'):
        course_ratings = []
        courses = university.courses.all()
         # Loop through courses and calculate ratings
        for course in courses:
            reviews = course.review_set.all()
            # Calculate the course rating as the average of the four review criteria
            if reviews:
                course_rating = (reviews.aggregate(
                    Avg('value_for_money'))['value_for_money__avg'] +
                                 reviews.aggregate(
                    Avg('teaching_quality'))['teaching_quality__avg'] +
                                 reviews.aggregate(
                    Avg('course_content'))['course_content__avg'] +
                                 reviews.aggregate(
                    Avg('job_prospects'))['job_prospects__avg']) / 4
                course_ratings.append(course_rating)
        if course_ratings:
            # Calculate the university rating as the average of all course ratings
            university_rating = sum(course_ratings) / len(course_ratings)
        else:
            university_rating = 0
        university_ratings[university] = university_rating

    context = {
        'university_ratings': university_ratings,
    }
    return render(request, 'campus/university_list.html', context)


def university_detail(request, university_name_slug):
    # Retrieve the University object with the matching slug, or return a 404 error if it doesn't exist.
    university = get_object_or_404(University, slug=university_name_slug)
    # Retrieve all courses that are associated with the university.
    courses = Course.objects.filter(university=university)
    course_ratings = []
    # Iterate through each course to retrieve the associated reviews and calculate the course rating
    for course in courses:
        reviews = course.review_set.all()
        if reviews:
            course_rating = (reviews.aggregate(
                Avg('value_for_money'))['value_for_money__avg'] +
                                 reviews.aggregate(
                    Avg('teaching_quality'))['teaching_quality__avg'] +
                                 reviews.aggregate(
                    Avg('course_content'))['course_content__avg'] +
                                 reviews.aggregate(
                    Avg('job_prospects'))['job_prospects__avg']) / 4
            course_ratings.append(course_rating)
    # Calculate the university rating by averaging the course ratings, if there are any
    if course_ratings:
        university_rating = sum(course_ratings) / len(course_ratings)
    else:
        university_rating = 0
    context = {
        'university': university,
        'courses': courses,
        'university_rating': university_rating,
    }
    return render(request, 'campus/university_detail.html', context)

def course_detail(request, course_name_slug):
    # Retrieves the course object with the given slug from the Course model, or raises a 404 error if it doesn't exist
    course = get_object_or_404(Course, slug=course_name_slug)
    # Filters all reviews related to this course from the Review model
    reviews = Review.objects.filter(course=course)
    # Calculates the overall rating for the course
    rating = 0
    if reviews:
        rating = (reviews.aggregate(Sum('value_for_money'))['value_for_money__sum'] +
                  reviews.aggregate(Sum('teaching_quality'))['teaching_quality__sum'] +
                  reviews.aggregate(Sum('course_content'))['course_content__sum'] +
                  reviews.aggregate(Sum('job_prospects'))['job_prospects__sum']) / (4 * reviews.count())

    return render(request, 'campus/course_detail.html', {'course': course, 'rating': rating, 'reviews': reviews})


class TopUniversitiesView(ListView):
    model = University
    template_name = 'campus/top_universities.html'
    context_object_name = 'top_universities'

    def get_queryset(self):
        universities = University.objects.all()
        university_ratings = {}

        for university in universities:
            course_ratings = []
            courses = university.courses.all()

            for course in courses:
                reviews = course.review_set.all()
                if reviews:
                    course_rating = (reviews.aggregate(Avg('value_for_money'))['value_for_money__avg'] +
                                     reviews.aggregate(Avg('teaching_quality'))['teaching_quality__avg'] +
                                     reviews.aggregate(Avg('course_content'))['course_content__avg'] +
                                     reviews.aggregate(Avg('job_prospects'))['job_prospects__avg']) / 4
                    course_ratings.append(course_rating)

            if course_ratings:
                university_rating = sum(course_ratings) / len(course_ratings)
                university_ratings[university] = university_rating
            else:
                university_ratings[university] = 0

        sorted_university_ratings = sorted(university_ratings.items(), key=lambda x: x[1], reverse=True)
        top_five_universities = sorted_university_ratings[:5]
        return top_five_universities
    

def contacting(request, course_name_slug):
    course = get_object_or_404(Course, slug=course_name_slug)
    return render(request, 'campus/Contacting.html', {'course': course})


def map(request):
    locations=Location.objects.all().values()
    locations = json.dumps( list(locations))
    return render(request, 'campus/Map.html', {'locations':locations})

def tip(request, course_name_slug):
    course = get_object_or_404(Course, slug=course_name_slug)
    return render(request, 'campus/Tip.html', {'course': course})