from rest_framework import serializers
from api.models import Tutorial

class TutorialSerializer(serializers.ModelSerializer):
	"""docstring for TutorialSerializer"""
	class Meta:
		#the model for Serialize
		model = Tutorial
		#a tuple of field names to be included in the serialization
		fields = (
				'id',
				'title',
				'description',
				'published'
			)
			
	
		