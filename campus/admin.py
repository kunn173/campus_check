from django.contrib import admin
from campus.models import Location, Degree, University, Course, User, Enrollment, Review

admin.site.register(Location)
admin.site.register(Degree)
admin.site.register(Enrollment)

# Add in this class to customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(name=request.user.username.replace("_", " "))
# Update the registration to include this customised interface


# class CourseAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         qs = super(CourseAdmin, self).get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(university=request.user.username.replace("_", " "))

# class ReviewAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         qs = super(ReviewAdmin, self).get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(university=request.user.username.replace("_", " "))


admin.site.register(University, CategoryAdmin)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Review, ReviewAdmin)
admin.site.register(Course)
admin.site.register(Review)
