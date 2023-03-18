from django.shortcuts import render, get_object_or_404
from .models import University, Course, Degree, Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment
from .forms import CourseReviewForm
from django.db.models import Avg, Sum


@login_required
def submit_review(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    try:
        enrollment = Enrollment.objects.get(user=user, courses=course)
    except Enrollment.DoesNotExist:
        enrollment = None

    if request.method == 'POST':
        form = CourseReviewForm(request.POST, course=course, user=user)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = user
            review.university = course.university
            review.save()
            return HttpResponseRedirect(reverse('universities:course_detail', args=[course.pk]))
    else:
        form = CourseReviewForm(course=course, user=user)

    return render(request, 'campus/submit_review.html', {'form': form, 'course': course, 'enrollment': enrollment})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
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
                return redirect('index')
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
    university_name = request.GET.get('university_name')
    city = request.GET.get('city')
    level_of_study = request.GET.get('level_of_study')
    course_name = request.GET.get('course_name')

    if university_name: # filter by university name
        universities = universities.filter(name__icontains=university_name)

    if city:
        universities = universities.filter(location__name__icontains=city)

    if level_of_study:
        degrees = Degree.objects.filter(name__icontains=level_of_study)
        universities = universities.filter(degree__in=degrees)

    if course_name:
        courses = Course.objects.filter(name__icontains=course_name)
        universities = universities.filter(courses__in=courses)

    university_ratings = {}
    for university in universities:
        course_ratings = []
        courses = university.courses.all()
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
        if course_ratings:
            university_rating = sum(course_ratings) / len(course_ratings)
            university_ratings[university] = university_rating

    context = {
        'university_ratings': university_ratings,
    }
    return render(request, 'campus/university_list.html', context)


def university_detail(request, pk):
    university = get_object_or_404(University, pk=pk)
    courses = Course.objects.filter(university=university)
    course_ratings = []
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
    if course_ratings:
        university_rating = sum(course_ratings) / len(course_ratings)
    else:
        university_rating = None
    context = {
        'university': university,
        'courses': courses,
        'university_rating': university_rating,
    }
    return render(request, 'campus/university_detail.html', context)



def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    reviews = Review.objects.filter(course=course)
    rating = 0
    if reviews:
        rating = (reviews.aggregate(Sum('value_for_money'))['value_for_money__sum'] +
                  reviews.aggregate(Sum('teaching_quality'))['teaching_quality__sum'] +
                  reviews.aggregate(Sum('course_content'))['course_content__sum'] +
                  reviews.aggregate(Sum('job_prospects'))['job_prospects__sum']) / (4 * reviews.count())

    return render(request, 'campus/course_detail.html', {'course': course, 'rating': rating, 'reviews': reviews})


