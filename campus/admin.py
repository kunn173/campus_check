from django.contrib import admin
from campus.models import Location, Degree, University, Course, User, Enrollment, Review

admin.site.register(Location)
admin.site.register(Degree)
admin.site.register(Enrollment)
admin.site.register(Review)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(name=request.user.username.replace("_", " "))
# Update the registration to include this customised interface
admin.site.register(University, CategoryAdmin)
admin.site.register(Course, CategoryAdmin)


