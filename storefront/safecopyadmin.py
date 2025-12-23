from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Field, Researcher

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'area', 'field_type', 'created_at')
    list_filter = ('domain', 'field_type')
    search_fields = ('name', 'domain', 'area')
    ordering = ('domain', 'name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Field Information', {
            'fields': ('name', 'domain', 'area', 'field_type')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'institution', 'country', 'total_star', 'peer_rating', 'get_expertise_count')
    list_filter = ('country', 'institution', 'created_at')
    search_fields = ('name', 'email', 'institution', 'interest')
    ordering = ('-total_star', 'name')
    filter_horizontal = ('expert_fields',)
    readonly_fields = ('researcher_id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('researcher_id', 'name', 'email', 'country', 'institution')
        }),
        ('Ratings & Metrics', {
            'fields': ('total_star', 'peer_rating')
        }),
        ('Research Profile', {
            'fields': ('interest', 'research_work', 'project', 'cv', 'github')
        }),
        ('Expertise (Relationship with Field)', {
            'fields': ('expert_fields',),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def get_expertise_count(self, obj):
        return obj.expert_fields.count()
    get_expertise_count.short_description = 'Expert Fields Count'