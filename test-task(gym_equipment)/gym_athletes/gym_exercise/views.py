from django.db.models import Sum
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Exercise
from .serializers import ExerciseSerializers


# Create your views here.


class ExerciseView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self,request):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        if start_date and end_date:
            query=Exercise.objects.filter(
                athlete=request.user, created_at__range=[start_date,end_date]).aggregate(Total_Calories=Sum('calories_burnt')
                )
            
        else:
            query= Exercise.objects.filter(athlete=request.user).aggregate(Total_Calories=Sum('calories_burnt'))
        query.update({
            "First Name": request.user.first_name,
            "Email": request.user.email
        })

        return Response(query)

    def post(self,request):
        serializer=ExerciseSerializers(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(athlete=request.user)
        return Response(serializer.data)





    


    
    









