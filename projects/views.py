from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Project
from .serializers import ProjectSerializer
import json  

class ProjectListView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_project_details(self, project_id):
        try:
            project = Project.objects.get(pk=project_id)
            serializer = ProjectSerializer(project)
            return JsonResponse(serializer.data, safe=False)

        except Project.DoesNotExist:
            return JsonResponse({'error': 'Not Found - The requested resource doesn\'t exist'}, status=404)

        except Exception as e:
            return JsonResponse({'error': 'Internal Server Error - {}'.format(str(e))}, status=500)


    def get(self, request, *args, **kwargs):
        # Handle headers and parameters
        api_key = request.headers.get('X-Binarybox-Api-Key', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('pageSize', 10))
        project_id = kwargs.get('project_id')

        # Validate API key
        if not self.validate_api_key(api_key):
            return JsonResponse({'error': 'Invalid API Key'}, status=403)

        if project_id is not None:
            # If project_id is provided, fetch the corresponding project details
            return self.get_project_details(project_id)

        try:
            # Fetch projects
            projects = Project.objects.all()[(page - 1) * page_size:page * page_size]
            serializer = ProjectSerializer(projects, many=True)

            return JsonResponse(serializer.data, safe=False)

        except ValueError as e:
            return JsonResponse({'error': 'Bad Request - {}'.format(str(e))}, status=400)

        except Project.DoesNotExist:
            return JsonResponse({'error': 'Not Found - The requested resource doesn\'t exist'}, status=404)

        except Exception as e:
            return JsonResponse({'error': 'Internal Server Error - {}'.format(str(e))}, status=500)
    
    def get_project(self, request, project_id, *args, **kwargs):
        # Handle headers
        api_key = request.headers.get('X-Binarybox-Api-Key', '')

        # Validate API key
        if not self.validate_api_key(api_key):
            return JsonResponse({'error': 'Invalid API Key'}, status=403)

        return self.get_project_details(project_id)

    
    
    def validate_api_key(self, api_key):
        # Add logic to validate the API key (e.g., check against a database)
        # For simplicity, let's assume a fixed API key for now.
        return api_key == 'abcdef123456'


    ##################################################### POST


    def post(self, request, *args, **kwargs):
        # Handle headers and parameters
        api_key = request.headers.get('X-Binarybox-Api-Key', '')

        # Validate API key
        if not self.validate_api_key(api_key):
            return JsonResponse({'error': 'Invalid API Key'}, status=403)

        try:
            print(request.body)  # Add this line to print the request body
            # Create a new project
            data = json.loads(request.body.decode('utf-8'))
            serializer = ProjectSerializer(data=data)

            if serializer.is_valid():
                project = serializer.save()
                return JsonResponse(serializer.data, status=201)
            else:
                return JsonResponse({'error': 'Bad Request - {}'.format(serializer.errors)}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Bad Request - Invalid JSON data'}, status=400)

        except Exception as e:
            return JsonResponse({'error': 'Internal Server Error - {}'.format(str(e))}, status=500)


##################################### Update

    def patch_project(self, request, project_id, *args, **kwargs):
        # Handle headers and parameters
        api_key = request.headers.get('X-Binarybox-Api-Key', '')

        # Validate API key
        if not self.validate_api_key(api_key):
            return JsonResponse({'error': 'Invalid API Key'}, status=403)

        try:
            # Fetch the project
            project = Project.objects.get(pk=project_id)

            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Update the project data
            serializer = ProjectSerializer(project, data=data, partial=True)
            
            if serializer.is_valid():
                project = serializer.save()
                return JsonResponse(serializer.data, status=200)
            else:
                return JsonResponse({'error': 'Bad Request - {}'.format(serializer.errors)}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Bad Request - Invalid JSON data'}, status=400)

        except Project.DoesNotExist:
            return JsonResponse({'error': 'Not Found - The requested resource doesn\'t exist'}, status=404)

        except Exception as e:
            return JsonResponse({'error': 'Internal Server Error - {}'.format(str(e))}, status=500)

    # ... existing methods ...

    def patch(self, request, project_id, *args, **kwargs):
        # Handle PATCH requests for updating a project
        return self.patch_project(request, project_id, *args, **kwargs)



    ####################################### DELETE

    def delete_project(self, request, project_id, *args, **kwargs):
        # Handle headers and parameters
        api_key = request.headers.get('X-Binarybox-Api-Key', '')

        # Validate API key
        if not self.validate_api_key(api_key):
            return JsonResponse({'error': 'Invalid API Key'}, status=403)

        try:
            # Fetch the project
            project = Project.objects.get(pk=project_id)

            # Delete the project
            project.delete()

            return JsonResponse({'message': 'Project deleted successfully'}, status=200)

        except Project.DoesNotExist:
            return JsonResponse({'error': 'Not Found - The requested resource doesn\'t exist'}, status=404)

        except Exception as e:
            return JsonResponse({'error': 'Internal Server Error - {}'.format(str(e))}, status=500)

    def delete(self, request, project_id, *args, **kwargs):
        # Handle DELETE requests for deleting a project
        return self.delete_project(request, project_id, *args, **kwargs)