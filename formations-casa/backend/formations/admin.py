from django.contrib import admin
from .models import Category, FormationType, Formation, Curriculum, FormationReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['is_active']


@admin.register(FormationType)
class FormationTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class CurriculumInline(admin.TabularInline):
    model = Curriculum
    extra = 1


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ['title', 'coach', 'category', 'delivery_mode', 'price', 'status', 'start_date']
    list_filter = ['status', 'delivery_mode', 'level', 'category']
    search_fields = ['title', 'coach__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CurriculumInline]
    date_hierarchy = 'start_date'


@admin.register(FormationReview)
class FormationReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'formation', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'formation__title']
