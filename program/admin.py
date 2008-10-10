from django.contrib import admin

from models import Author, Proposal, Review

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email')

class ProposalAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'status', 'reviews_count', 'submitted')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'reviewer', 'reviewed')

    def queryset(self, request):
        queryset = super(ReviewAdmin, self).queryset(request)

        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(reviewer=request.user)

    def save_model(self, request, obj, form, change):
        obj.reviewer = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser or obj.reviewer==request.user:
            return True
        else:
            return False

    has_delete_permission = has_change_permission

admin.site.register(Author, AuthorAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Review, ReviewAdmin)
