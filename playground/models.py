# models.py - FIXED VERSION (All related_name conflicts resolved)
# Replace your entire models.py with this

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# ============================================================================
# ENTITY 1: FIELD
# ============================================================================
class Field(models.Model):
    """Research field/domain"""
    name = models.CharField(max_length=200, primary_key=True)
    domain = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    field_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'field'
        ordering = ['domain', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.domain})"


# ============================================================================
# ENTITY 2: SUBFIELD
# ============================================================================
class Subfield(models.Model):
    """Subfield within a research field"""
    name = models.CharField(max_length=200, primary_key=True)
    field_type = models.CharField(max_length=100)
    domain = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # RELATIONSHIP: Subfield (M) → BELONGS → Field (1)
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='subfields'
    )
    
    class Meta:
        db_table = 'subfield'
        ordering = ['field', 'name']
    
    def __str__(self):
        return f"{self.name} (under {self.field.name})"


# ============================================================================
# ENTITY 3: PROBLEM
# ============================================================================
class Problem(models.Model):
    """Research problem"""
    name = models.CharField(max_length=200, primary_key=True)
    current_proceedings = models.TextField()
    ongoing_work = models.TextField(blank=True)
    done_work = models.TextField(blank=True)
    funding_reserves = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    list_of_researchers_working = models.TextField(blank=True)
    description = models.TextField()
    severity_color = models.CharField(
        max_length=50,
        choices=[
            ('green', 'Low Priority'),
            ('yellow', 'Medium Priority'),
            ('orange', 'High Priority'),
            ('red', 'Critical Priority'),
        ],
        default='yellow'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # RELATIONSHIP: Problem (M) → BELONGS → Subfield (1)
    subfield = models.ForeignKey(
        Subfield,
        on_delete=models.CASCADE,
        related_name='problems'
    )
    
    class Meta:
        db_table = 'problem'
        ordering = ['severity_color', 'name']
    
    def __str__(self):
        return f"{self.name} [{self.severity_color.upper()}]"


# ============================================================================
# ENTITY 4: RESEARCHER
# ============================================================================
class Researcher(models.Model):
    """Researcher with profile and expertise"""
    researcher_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    institution = models.CharField(max_length=300)
    total_star = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    peer_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    interest = models.TextField()
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    research_work = models.TextField(blank=True)
    project = models.TextField(blank=True)
    github = models.URLField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # RELATIONSHIP: Researcher (1) → EXPERT → Field (M)
    expert_fields = models.ManyToManyField(
        Field,
        related_name='expert_researchers',
        blank=True
    )
    
    # RELATIONSHIP: Researcher (M) → FRIENDS WITH → Researcher (N) - Self-referential M:N
    # FIXED: Removed related_name since symmetrical=True
    friends = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=True
    )
    
    class Meta:
        db_table = 'researcher'
        ordering = ['-total_star', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.institution})"


# ============================================================================
# ENTITY 5: RESEARCH WORK
# ============================================================================
class ResearchWork(models.Model):
    """Published research work/paper"""
    work_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    author_name = models.CharField(max_length=300)
    publisher = models.CharField(max_length=200)
    citation = models.IntegerField(default=0)
    status = models.CharField(
        max_length=50,
        choices=[
            ('published', 'Published'),
            ('under_review', 'Under Review'),
            ('in_progress', 'In Progress'),
            ('draft', 'Draft'),
        ],
        default='draft'
    )
    vacancy_status = models.BooleanField(default=False, help_text="Open for collaboration")
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # RELATIONSHIP: ResearchWork (M) → WORKS → Researcher (N)
    researchers = models.ManyToManyField(
        Researcher,
        related_name='research_works',
        blank=True
    )
    
    # RELATIONSHIP: ResearchWork (1) → SOLVES → Problem (1)
    solves_problem = models.OneToOneField(
        Problem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solved_by_research'
    )
    
    # RELATIONSHIP: ResearchWork (M) → BELONGS → Subfield (1)
    subfield = models.ForeignKey(
        Subfield,
        on_delete=models.CASCADE,
        related_name='research_works'
    )
    
    class Meta:
        db_table = 'research_work'
        ordering = ['-citation', 'title']
    
    def __str__(self):
        return f"{self.title} (Citations: {self.citation})"


# ============================================================================
# ENTITY 6: FUNDING INSTITUTION
# ============================================================================
class FundingInstitution(models.Model):
    """Institution that provides funding"""
    institution_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    country = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'funding_institution'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.country})"


# ============================================================================
# ENTITY 7: POSTS (Abstract Superclass)
# ============================================================================
class Posts(models.Model):
    """Abstract base class for all post types"""
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True  # This makes it a superclass
        ordering = ['-created_at']


# ============================================================================
# ENTITY 7a: PROJECT COLAB (Subclass of Posts)
# ============================================================================
class ProjectColab(Posts):
    """Project collaboration post"""
    project_name = models.CharField(max_length=200)
    required_skills = models.TextField()
    duration = models.CharField(max_length=100)
    
    # RELATIONSHIP: ProjectColab (M) → POSTED BY → Researcher (1)
    # Each subclass needs its own unique related_name
    posted_by = models.ForeignKey(
        Researcher,
        on_delete=models.CASCADE,
        related_name='project_colabs'
    )
    
    class Meta:
        db_table = 'project_colab'
        verbose_name = 'Project Collaboration'
        verbose_name_plural = 'Project Collaborations'
    
    def __str__(self):
        return f"Project: {self.project_name}"


# ============================================================================
# ENTITY 7b: QUERY POST (Subclass of Posts)
# ============================================================================
class QueryPost(Posts):
    """Research query/question post"""
    query_type = models.CharField(
        max_length=50,
        choices=[
            ('technical', 'Technical'),
            ('research', 'Research'),
            ('general', 'General'),
        ],
        default='general'
    )
    is_answered = models.BooleanField(default=False)
    
    # RELATIONSHIP: QueryPost (M) → POSTED BY → Researcher (1)
    # Each subclass needs its own unique related_name
    posted_by = models.ForeignKey(
        Researcher,
        on_delete=models.CASCADE,
        related_name='query_posts'
    )
    
    # RELATIONSHIP: Researcher (M) → FEEDBACK → QueryPost (N)
    feedback_from = models.ManyToManyField(
        Researcher,
        related_name='feedback_queries',
        blank=True
    )
    
    class Meta:
        db_table = 'query_post'
        verbose_name = 'Query Post'
        verbose_name_plural = 'Query Posts'
    
    def __str__(self):
        return f"Query: {self.title}"


# ============================================================================
# ENTITY 7c: FUNDING PROPOSAL (Subclass of Posts)
# ============================================================================
class FundingProposal(Posts):
    """Funding proposal post"""
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    proposal_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('under_review', 'Under Review'),
        ],
        default='pending'
    )
    
    # RELATIONSHIP: FundingProposal (M) → POSTED BY → Researcher (1)
    # Each subclass needs its own unique related_name
    posted_by = models.ForeignKey(
        Researcher,
        on_delete=models.CASCADE,
        related_name='funding_proposals_posted'
    )
    
    # RELATIONSHIP: FundingProposal (M) → POSTED BY → FundingInstitution (1)
    funding_institution = models.ForeignKey(
        FundingInstitution,
        on_delete=models.CASCADE,
        related_name='proposals'
    )
    
    # RELATIONSHIP: FundingProposal (M) → FOR → ResearchWork (1)
    research_work = models.ForeignKey(
        ResearchWork,
        on_delete=models.CASCADE,
        related_name='funding_proposals',
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'funding_proposal'
        verbose_name = 'Funding Proposal'
        verbose_name_plural = 'Funding Proposals'
    
    def __str__(self):
        return f"Proposal: {self.title} (${self.requested_amount})"


# ============================================================================
# ENTITY 8: CONVERSATION
# ============================================================================
class Conversation(models.Model):
    """Conversation thread"""
    conversation_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Participants (M:N)
    participants = models.ManyToManyField(
        Researcher,
        related_name='conversations',
        blank=True
    )
    
    class Meta:
        db_table = 'conversation'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversation #{self.conversation_id}"


# ============================================================================
# ENTITY 9: MSG (Message)
# ============================================================================
class Message(models.Model):
    """Message in a conversation"""
    message_id = models.AutoField(primary_key=True)
    body = models.TextField()
    time_date = models.DateTimeField(auto_now_add=True)
    
    # RELATIONSHIP: Message (M) → SENT BY → Researcher (1)
    sender = models.ForeignKey(
        Researcher,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    
    # RELATIONSHIP: Message (M) → SENT TO → Researcher (1)
    receiver = models.ForeignKey(
        Researcher,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    
    # RELATIONSHIP: Message (M) → GROUPS → Conversation (1)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    class Meta:
        db_table = 'message'
        ordering = ['time_date']
    
    def __str__(self):
        return f"Message from {self.sender.name} at {self.time_date}"


# ============================================================================
# ENTITY 10: COMMENT (Abstract Superclass)
# ============================================================================
class Comment(models.Model):
    """Abstract base class for comments (Mentor and CoWorker)"""
    comment_id = models.AutoField(primary_key=True)
    content = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True  # Superclass
        ordering = ['-created_at']


# ============================================================================
# ENTITY 10a: MENTOR (Subclass of Comment - Disjoint)
# ============================================================================
class Mentor(Comment):
    """Mentor comment type"""
    punctual_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5
    )
    consistency = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5
    )
    hard_working = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5
    )
    
    # TERNARY RELATIONSHIP: Researcher ↔ ResearchWork ↔ Mentor Comment
    # Each subclass needs its own unique related_name
    researcher = models.ForeignKey(
        Researcher,
        on_delete=models.CASCADE,
        related_name='mentor_comments'
    )
    research_work = models.ForeignKey(
        ResearchWork,
        on_delete=models.CASCADE,
        related_name='mentor_comments'
    )
    
    class Meta:
        db_table = 'mentor'
        verbose_name = 'Mentor Comment'
        verbose_name_plural = 'Mentor Comments'
    
    def __str__(self):
        return f"Mentor Comment by {self.researcher.name}"


# ============================================================================
# ENTITY 10b: CO-WORKER (Subclass of Comment - Disjoint)
# ============================================================================
class CoWorker(Comment):
    """Co-worker comment type"""
    strength = models.TextField()
    hard_working = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5
    )
    
    # TERNARY RELATIONSHIP: Researcher ↔ ResearchWork ↔ CoWorker Comment
    # Each subclass needs its own unique related_name
    researcher = models.ForeignKey(
        Researcher,
        on_delete=models.CASCADE,
        related_name='coworker_comments'
    )
    research_work = models.ForeignKey(
        ResearchWork,
        on_delete=models.CASCADE,
        related_name='coworker_comments'
    )
    
    class Meta:
        db_table = 'coworker'
        verbose_name = 'Co-Worker Comment'
        verbose_name_plural = 'Co-Worker Comments'
    
    def __str__(self):
        return f"Co-Worker Comment by {self.researcher.name}"


# ============================================================================
# TERNARY RELATIONSHIP: Researcher ↔ FundingInstitution ↔ ResearchWork (COLAB)
# ============================================================================
class Collaboration(models.Model):
    """Ternary relationship: Researcher, Funding Institution, and Research Work collaboration"""
    collaboration_id = models.AutoField(primary_key=True)
    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    funding_institution = models.ForeignKey(FundingInstitution, on_delete=models.CASCADE)
    research_work = models.ForeignKey(ResearchWork, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    contribution_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    class Meta:
        db_table = 'collaboration'
        unique_together = ['researcher', 'funding_institution', 'research_work']
    
    def __str__(self):
        return f"{self.researcher.name} ↔ {self.funding_institution.name} ↔ {self.research_work.title}"