
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from gym_exercise.models import Exercise, GymEquipment


user_data = {
    "username": "athelete",
    "email": "athelete@gmail.com",
    "password": "athelete@123"
}

equipment_data = {
    "name": "Treadmills"
}

exercise_data = {
    'athlete' :  1 ,
    'gym_equipment' : 1 ,
    'duration' :  '10' ,
    'description' : 'Testing' ,
    'calories_burnt' : 10,
    'created_at' : '2022-12-16'
}

payload = {
    "username":"athelete",
    "password":"athelete@123"
}

def user_login(client):
    client.post(reverse("api_token_auth"), payload)

class TestAthelete(APITestCase):
    def setUp(self):
        self.user = User.objects.create(**user_data)
        self.equipment = GymEquipment.objects.create(**equipment_data)

        exercise_data['athlete'] = self.user
        exercise_data['gym_equipment'] = self.equipment
        self.exercise = Exercise.objects.create(**exercise_data)
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.exercise_url = reverse("exercise")

    
    def test_create_exercise_success(self):
        exercise_data['gym_equipment'] = self.equipment.id
        response = self.client.post(self.exercise_url, exercise_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['gym_equipment'], exercise_data['gym_equipment'])

    def test_create_exercise_failure(self):
        del exercise_data['gym_equipment']
        response = self.client.post(self.exercise_url, exercise_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_calories_with_invalid_dates(self):
        response = self.client.get(f'{self.exercise_url}?start_date=2022-12-12&end_date=2022-12-15')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Total_Calories'], None)

    def test_get_calories_with_valid_dates(self):
        response = self.client.get(f'{self.exercise_url}?start_date=2022-12-15&end_date=2022-12-17')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Total_Calories'], exercise_data['calories_burnt'])


    def tearDown(self):
        self.user.delete()
        self.equipment.delete()
