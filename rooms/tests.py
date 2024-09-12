from rest_framework.test import APITestCase
from . import models
from users.models import User

class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Desc"
    URL = "/api/v1/rooms/amenities/"
    
    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESC)
    
    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()
        self.assertEqual(response.status_code, 200, "Not 200")
        # 누구나 접근하여 status_code가 200인지 여부를 확인(authentication X) 
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESC)
        
    def test_create_amenity(self):
        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity Desc."
        response = self.client.post(self.URL, data={"name": new_amenity_name, "description": new_amenity_description},)
        data = response.json()
        self.assertEqual(response.status_code, 200, "Not 200")
        self.assertEqual(data["name"], new_amenity_name,)
        self.assertEqual(data["description"], new_amenity_description)
        
        response = self.client.post(self.URL)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)

class TestAmenity(APITestCase):
    NAME = "Test Amenity"
    DESC = "Test Desc"
    
    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESC,)
    
    def test_amenity_not_found(self):
        # amenity가 없는 경우 
        response = self.client.get("/api/v1/rooms/amenities/2")
        self.assertEqual(response.status_code, 404)
    
    def test_get_amenity(self):
        # amenity가 있는 경우 
        response = self.client.get("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["name"], self.NAME,)
        self.assertEqual(data["description"], self.DESC,)
    
    def test_put_amenity(self):
        response = self.client.put(
            "/api/v1/rooms/amenities/1",
            data={"name": self.NAME, "description": self.DESC},
        )

        data = response.json()
        self.assertEqual(data["name"], self.NAME)
        self.assertEqual(data["description"], self.DESC)
        self.assertEqual(response.status_code, 200)

        name_len_200 = 'a' * 200
        name_validate_response = self.client.put(
            "/api/v1/rooms/amenities/1",
            data={"name": name_len_200},
        )
        data = name_validate_response.json()
        self.assertIn('name', data)
        self.assertNotIn('decs', data)
        self.assertEqual(name_validate_response.status_code, 400)
    
    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 204)


class TestRooms(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test",)   # 유저 생성
        user.set_password("123")
        user.save()
        self.user = user
    
    def test_create_room(self):
        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(response.status_code, 403)
        
        self.client.force_login(self.user,)  # 이제 로그인 됨 
        
        response = self.client.post("/api/v1/rooms/")
        print(response.json())