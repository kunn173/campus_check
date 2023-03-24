from django import forms
from .models import Review, Enrollment, StudentProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Review

class CourseReviewForm(forms.ModelForm):
    value_for_money = forms.ChoiceField(choices=[(i, '') for i in range(1, 6)],
                                        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
                                        label='Value for Money')
    teaching_quality = forms.ChoiceField(choices=[(i, '') for i in range(1, 6)],
                                         widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
                                         label='Teaching Quality')
    course_content = forms.ChoiceField(choices=[(i, '') for i in range(1, 6)],
                                       widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
                                       label='Course Content')
    job_prospects = forms.ChoiceField(choices=[(i, '') for i in range(1, 6)],
                                      widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
                                      label='Job Prospects')
    review_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Review
        fields = ('value_for_money', 'teaching_quality', 'course_content', 'job_prospects', 'review_text')

    def __init__(self, *args, **kwargs):
        self.course = kwargs.pop('course')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        enrollment = Enrollment.objects.filter(user=self.user, courses=self.course).first()
        if not enrollment:
            raise forms.ValidationError("You cannot review a course that you have not enrolled in.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        instance.university = self.course.university
        instance.course = self.course
        if commit:
            instance.save()
        return instance

def get_or_create_student_profile(user):
    student_profile, created = StudentProfile.objects.get_or_create(user=user)
    if created:
        student_profile.email = user.email
        student_profile.first_name = user.first_name
        student_profile.last_name = user.last_name
        student_profile.save()
    return student_profile

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(StudentRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()

        student_profile, created = StudentProfile.objects.get_or_create(user=user)
        student_profile.email = user.email
        student_profile.first_name = user.first_name
        student_profile.last_name = user.last_name
        student_profile.date_of_birth = self.cleaned_data['date_of_birth']
        student_profile.save()

        return user


class StudentProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = StudentProfile
        fields = ('email', 'first_name', 'last_name', 'date_of_birth')
