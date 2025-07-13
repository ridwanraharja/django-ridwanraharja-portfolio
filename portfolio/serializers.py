from rest_framework import serializers
from .models import Portfolio, PortfolioImage

class PortfolioImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioImage
        fields = ['id', 'image', 'caption', 'order']

class PortfolioSerializer(serializers.ModelSerializer):
    images = PortfolioImageSerializer(many=True, read_only=True)
    technologies_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Portfolio
        fields = ['id', 'title', 'description', 'technologies', 'technologies_list', 
                 'image', 'images', 'live_url', 'github_url', 'created_at', 
                 'is_featured', 'order']
    
    def get_technologies_list(self, obj):
        return [tech.strip() for tech in obj.technologies.split(',') if tech.strip()]