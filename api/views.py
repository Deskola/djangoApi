from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from api.models import Tutorial
from api.serializers import TutorialSerializer
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET', 'DELETE', 'POST'])
def tutorial_list(request):
	# GET list of tutorials, POST a new tutorial, DELETE all tutorials

	if request.method == 'GET':
		tutorials = Tutorial.objects.all()

		title = request.GET.get('title', None)
		if title is not None:
			tutorials = tutorials.filter(title__icontains=title)

		tutorial_serializer = TutorialSerializer(tutorials, many=True)

		# 'safe=False' for objects serialization
		return JsonResponse(tutorial_serializer.data, safe=False)
		
	elif request.method == 'POST':
		#create and save a new Tutorial
		tutorial_data = JSONParser().parse(request)
		tutorial_serializer = TutorialSerializer(data = tutorial_data)
		if tutorial_serializer.is_valid():
			tutorial_serializer.save()
			return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
		return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		count = Tutorial.objects.all().delete()
		return JsonResponse({'message': f'{count[0]} Tutorials were deleted successfully!'}, status=status.HTTP_204_NO_CONTENT )

@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
	#find tutorial by pk(id)
	try:
		tutorial = Tutorial.objects.get(pk=pk)
	except Tutorial.DoesNotExit:
		return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)

	# GET / PUT / DELETE tutorial
	if request.method == 'GET':
		tutorial_serializer = TutorialSerializer(tutorial)
		return JsonResponse(tutorial_serializer.data)

	elif request.method == 'PUT':
		tutorial_data = JSONParser().parse(request)
		tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data)

		if tutorial_serializer.is_valid():
			tutorial_serializer.save()
			return JsonResponse(tutorial_serializer.data)
		return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

	elif request.method == 'DELETE':
		tutorial.delete()
		return JsonResponse({'message': "Tutorial was deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

	
		

@api_view(['GET'])
def tutorial_list_published(request):
	# GET all published tutorials
	tutorials = Tutorial.objects.filter(published=True)

	if request.method == 'GET':
		tutorial_serializer = TutorialSerializer(tutorials, many=True)
		return JsonResponse(tutorial_serializer.data, safe=False)

	
