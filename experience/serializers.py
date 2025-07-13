from rest_framework import serializers
from .models import Experience

class ExperienceSerializer(serializers.ModelSerializer):
    skills_list = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Experience
        fields = ['id', 'title', 'company_or_institution', 'location', 'description',
                 'start_date', 'end_date', 'is_current', 'experience_type', 
                 'skills', 'skills_list', 'duration', 'order']
    
    def get_skills_list(self, obj):
        if obj.skills:
            return [skill.strip() for skill in obj.skills.split(',') if skill.strip()]
        return []
    
    def get_duration(self, obj):
        if obj.is_current:
            return f"{obj.start_date.strftime('%B %Y')} - Present"
        elif obj.end_date:
            return f"{obj.start_date.strftime('%B %Y')} - {obj.end_date.strftime('%B %Y')}"
        return obj.start_date.strftime('%B %Y')