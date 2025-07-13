from django.db import models

class Experience(models.Model):
    EXPERIENCE_TYPES = [
        ('work', 'Work Experience'),
        ('education', 'Education'),
        ('project', 'Project'),
        ('certification', 'Certification'),
    ]
    
    title = models.CharField(max_length=200)
    company_or_institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPES, default='work')
    skills = models.CharField(max_length=500, blank=True)  # JSON string
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return f"{self.title} at {self.company_or_institution}"