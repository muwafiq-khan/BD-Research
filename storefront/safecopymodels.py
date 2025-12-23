from django.db import models

# Create your models here.
from django.db import models


class Field(models.Model):
    """
    Represents a research field/domain
    """
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


class Researcher(models.Model):
    """
    Represents a researcher with their profile and expertise
    """
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
    
    # RELATIONSHIP: RESEARCHER (1) → EXPERT → FIELD (M)
    expert_fields = models.ManyToManyField(
        Field,
        related_name='expert_researchers',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'researcher'
        ordering = ['-total_star', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.institution})"
    
    def get_expertise_summary(self):
        return ", ".join([field.name for field in self.expert_fields.all()])