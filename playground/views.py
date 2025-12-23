# views.py
# Add this to your playground/views.py

from django.shortcuts import render
from django.db.models import Q
from .models import Field, Subfield

def field_search(request):
    """
    Search for fields and display their subfields
    """
    query = request.GET.get('q', '')  # Get search query from URL parameter
    fields = []
    subfields_by_field = {}
    
    if query:
        # Search for fields that match the query (case-insensitive)
        fields = Field.objects.filter(
            Q(name__icontains=query) | 
            Q(domain__icontains=query) | 
            Q(area__icontains=query)
        )
        
        # For each field found, get its subfields
        for field in fields:
            subfields = field.subfields.all()  # Using the related_name we defined
            subfields_by_field[field] = subfields
    
    context = {
        'query': query,
        'fields': fields,
        'subfields_by_field': subfields_by_field,
    }
    
    return render(request, 'playground/field_search.html', context)


def home(request):
    """
    Home page with search box
    """
    return render(request, 'playground/home.html')