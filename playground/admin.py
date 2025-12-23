# admin.py - COMPLETE VERSION WITH ALL ENTITIES
# Replace your entire admin.py with this

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Field, Subfield, Problem, Researcher, ResearchWork,
    FundingInstitution, ProjectColab, QueryPost, FundingProposal,
    Conversation, Message, Mentor, CoWorker, Collaboration
)

# ============================================================================
# FIELD ADMIN
# ============================================================================
@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'area', 'field_type', 'subfield_count')
    list_filter = ('domain', 'field_type')
    search_fields = ('name', 'domain', 'area')
    
    def subfield_count(self, obj):
        return obj.subfields.count()
    subfield_count.short_description = 'Subfields'


# ============================================================================
# SUBFIELD ADMIN
# ============================================================================
@admin.register(Subfield)
class SubfieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'field', 'field_type', 'domain', 'problem_count')
    list_filter = ('field', 'field_type')
    search_fields = ('name', 'field__name')
    
    def problem_count(self, obj):
        return obj.problems.count()
    problem_count.short_description = 'Problems'


# ============================================================================
# PROBLEM ADMIN
# ============================================================================
@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'subfield', 'severity_display', 'funding_reserves', 'has_solution')
    list_filter = ('severity_color', 'subfield')
    search_fields = ('name', 'description')
    
    def severity_display(self, obj):
        colors = {
            'green': '#28a745',
            'yellow': '#ffc107',
            'orange': '#fd7e14',
            'red': '#dc3545'
        }
        color = colors.get(obj.severity_color, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {}</span>',
            color,
            obj.get_severity_color_display()
        )
    severity_display.short_description = 'Priority'
    
    def has_solution(self, obj):
        return hasattr(obj, 'solved_by_research') and obj.solved_by_research is not None
    has_solution.boolean = True
    has_solution.short_description = 'Solved?'


# ============================================================================
# RESEARCHER ADMIN
# ============================================================================
@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'institution', 'country', 'total_star', 'expert_count', 'friends_count')
    list_filter = ('country', 'institution')
    search_fields = ('name', 'email', 'institution')
    filter_horizontal = ('expert_fields', 'friends')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'email', 'country', 'institution')
        }),
        ('Ratings', {
            'fields': ('total_star', 'peer_rating')
        }),
        ('Profile', {
            'fields': ('interest', 'research_work', 'project', 'cv', 'github')
        }),
        ('Relationships', {
            'fields': ('expert_fields', 'friends')
        }),
    )
    
    def expert_count(self, obj):
        return obj.expert_fields.count()
    expert_count.short_description = 'Expert Fields'
    
    def friends_count(self, obj):
        return obj.friends.count()
    friends_count.short_description = 'Friends'


# ============================================================================
# RESEARCH WORK ADMIN
# ============================================================================
@admin.register(ResearchWork)
class ResearchWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'status', 'citation', 'vacancy_status', 'researcher_count')
    list_filter = ('status', 'vacancy_status', 'subfield')
    search_fields = ('title', 'author_name', 'name')
    filter_horizontal = ('researchers',)
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'name', 'author_name', 'publisher')
        }),
        ('Status', {
            'fields': ('status', 'vacancy_status', 'citation')
        }),
        ('Relationships', {
            'fields': ('subfield', 'solves_problem', 'researchers')
        }),
    )
    
    def researcher_count(self, obj):
        return obj.researchers.count()
    researcher_count.short_description = 'Researchers'


# ============================================================================
# FUNDING INSTITUTION ADMIN
# ============================================================================
@admin.register(FundingInstitution)
class FundingInstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'amount', 'budget', 'proposal_count')
    list_filter = ('country',)
    search_fields = ('name', 'country')
    
    def proposal_count(self, obj):
        return obj.proposals.count()
    proposal_count.short_description = 'Proposals'


# ============================================================================
# PROJECT COLAB ADMIN
# ============================================================================
@admin.register(ProjectColab)
class ProjectColabAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'posted_by', 'duration', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('project_name', 'title', 'posted_by__name')
    
    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'content', 'posted_by')
        }),
        ('Project Details', {
            'fields': ('project_name', 'required_skills', 'duration')
        }),
    )


# ============================================================================
# QUERY POST ADMIN
# ============================================================================
@admin.register(QueryPost)
class QueryPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'query_type', 'is_answered', 'feedback_count', 'created_at')
    list_filter = ('query_type', 'is_answered', 'created_at')
    search_fields = ('title', 'content', 'posted_by__name')
    filter_horizontal = ('feedback_from',)
    
    def feedback_count(self, obj):
        return obj.feedback_from.count()
    feedback_count.short_description = 'Feedback Count'


# ============================================================================
# FUNDING PROPOSAL ADMIN
# ============================================================================
@admin.register(FundingProposal)
class FundingProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'funding_institution', 'requested_amount', 'proposal_status', 'created_at')
    list_filter = ('proposal_status', 'funding_institution', 'created_at')
    search_fields = ('title', 'posted_by__name')
    
    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'content', 'posted_by')
        }),
        ('Proposal Details', {
            'fields': ('requested_amount', 'proposal_status', 'funding_institution', 'research_work')
        }),
    )


# ============================================================================
# CONVERSATION ADMIN
# ============================================================================
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'title', 'participant_count', 'message_count', 'updated_at')
    search_fields = ('title',)
    filter_horizontal = ('participants',)
    
    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = 'Participants'
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


# ============================================================================
# MESSAGE ADMIN
# ============================================================================
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'receiver', 'conversation', 'time_date', 'body_preview')
    list_filter = ('time_date',)
    search_fields = ('body', 'sender__name', 'receiver__name')
    
    def body_preview(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body
    body_preview.short_description = 'Message Preview'


# ============================================================================
# MENTOR ADMIN
# ============================================================================
@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('researcher', 'research_work', 'rating', 'punctual_score', 'consistency', 'hard_working', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('researcher__name', 'research_work__title', 'content')
    
    fieldsets = (
        ('Comment Info', {
            'fields': ('researcher', 'research_work', 'content', 'rating')
        }),
        ('Mentor Scores', {
            'fields': ('punctual_score', 'consistency', 'hard_working')
        }),
    )


# ============================================================================
# CO-WORKER ADMIN
# ============================================================================
@admin.register(CoWorker)
class CoWorkerAdmin(admin.ModelAdmin):
    list_display = ('researcher', 'research_work', 'rating', 'hard_working', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('researcher__name', 'research_work__title', 'content', 'strength')
    
    fieldsets = (
        ('Comment Info', {
            'fields': ('researcher', 'research_work', 'content', 'rating')
        }),
        ('Co-Worker Evaluation', {
            'fields': ('strength', 'hard_working')
        }),
    )


# ============================================================================
# COLLABORATION ADMIN (Ternary Relationship)
# ============================================================================
@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('researcher', 'funding_institution', 'research_work', 'contribution_amount', 'start_date', 'end_date')
    list_filter = ('start_date', 'funding_institution')
    search_fields = ('researcher__name', 'funding_institution__name', 'research_work__title')
    
    fieldsets = (
        ('Collaboration Parties', {
            'fields': ('researcher', 'funding_institution', 'research_work')
        }),
        ('Timeline & Contribution', {
            'fields': ('start_date', 'end_date', 'contribution_amount')
        }),
    )