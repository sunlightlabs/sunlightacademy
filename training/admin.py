from django.contrib import admin
from training.models import Profile, Category, Module, Completion, Training, Feedback


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description', 'is_public')
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Module, ModuleAdmin)


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'end_time', 'category', 'is_public')
    list_editable = ('is_public',)
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Training, TrainingAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'module')
admin.site.register(Feedback, FeedbackAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'is_a')
    list_filter = ('is_a',)
admin.site.register(Profile, ProfileAdmin)

admin.site.register(Completion)
