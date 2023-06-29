from decimal import Decimal

from django.db import transaction
from projects.models import Project
from projects.rest.serializers import ProjectSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination



class ProjectViewSet(viewsets.ModelViewSet):
    # queryset = Project.objects.order_by("-start_date")     - remove query becz it is not working for given condition
  
    queryset = (
        Project.objects.select_related("company")
        .prefetch_related("company__tags")                
    ) 

    # optimize and improve performance by reducing the number of SQL queries
    serializer_class = ProjectSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated]


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        with transaction.atomic():
            data = {
                "actual_development": instance.actual_development
                + Decimal(request.data["actual_development"]),
                "actual_design": instance.actual_design
                + Decimal(request.data["actual_design"]),
                "actual_testing": instance.actual_testing
                + Decimal(request.data["actual_testing"]),
            }
            serializer = self.serializer_class(instance, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
