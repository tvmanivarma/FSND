import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor
from dotenv import load_dotenv

load_dotenv()

database_name = "castingagency_test"
base_path = os.environ["DATABASE_PATH"]
database_path='{}/{}'.format(base_path, database_name)

# Valid JWT Token for Assistant 
Assistant = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Mjg5MDMyMzk2MWM5ZDAwNjhhMjQxMDgiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3Nzg3NDA1LCJleHAiOjE2NTc4NzM4MDUsImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.LisjREAAkE4ciGOvVqJs7n4LK4Gj884Jyqq8BzflvWqYZZgiPWixoE2YAZlG9cMeKH1SVDOhQ6Sf9uIxzd3gFRrP9kpVtvNshjpZ0Fm0b09u853_B4Ss4AOqYHUBqf8ubF_SnICUaj2kl7ofUIOpnpVrG7wixry9f6ssLLEPwqgHQA3WOVagyAqk7XDj4KCW67kL2yzP8lQBQv6PnzQzrR8OGdqSeu5uw_-lzPPwKhxE60mPPJCkMNsDKC6zJSGwP_AS3DAwnSjdNnRLpYvXtgpOQbpxo8hyqc7odhcOVgHfYOeiVuZ7JTGknuodhePsmqEs35b38a4FIvRoj0p2ww')
# Expired / Invalid JWT Token for Assistant 
Assistant_invalid = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Mjg5MDMyMzk2MWM5ZDAwNjhhMjQxMDgiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3NTA3MjgxLCJleHAiOjE2NTc1MjUyODEsImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.YfQWrTS26u3Bqnr-jQJb59EIB8V3WcZHaabW9XDB7lsMPa7X8jMg-Q9P9atcVJNZRjDL9mjqvy6bipBqYWmPYGaLI2QkNI05MuzNYdezgZiUaLQrvXm6_LO7DNn2dKzu6hzeQEdkTQ7eI6-piKozcHkt9trgKSDlqcEBms-syRr6_5HhmX_Yh9Q4ygbjLkGI-eKuXcYhmVIWj1N1dCfquxput4n-l4Srg_OCv2d2EQ4YU4rlgrPCbdwkLgohvigoUW02YurLNR86QWhyF-KlAwKtmUjN1cpfTsCdLuGzgEpZRNr4xQeG2qKWYuaAV9MMLrqWJTYuNgl2_YXrfolqOg')

# Valid JWT Token for Director
Director = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Mjg5MDJjZGQxZWI2ZjAwNjhkMTljNzkiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3Nzg3NzUyLCJleHAiOjE2NTc4NzQxNTIsImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.hNVQYdqExc5_iu0BP5ZGzFk_rOQn8oGPHqdMcQyhLiuGhQysDCdijay4o3W8fxikfnn-DImVIbzTwhJMNVwz4xqcLBy6eMbMv2yEqN8SuVm8dvmywokUvieuOtsjYyyr4iySjrF3_FeXaOO-D6C9RFAigfYEszPVmw02nVgxjjXUyzfC7tnk1hXaHICh6hdWpkTpG1bR9enK1yhFpX824KiDYAZ1rvVmgQbFVSurY5pRRZJNVcIzRwdwcFQEemOsIQvn5w-Dntoy5jQ56fMUI0IjRNRFJimBoUPBKE1QV4HNM8-9O-TPcAWySX8rPezlDSU4VUVS3YsEBI0P2nn0HQ')
# Expired / Invalid JWT Token for Director
Director_invalid = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Mjg5MDJjZGQxZWI2ZjAwNjhkMTljNzkiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3NDg1MzY5LCJleHAiOjE2NTc1MDMzNjksImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.g2eaQN_wXKL-1rfWND9RB0V-Bvp-TlsnNxWbG5OIkn-9OOcqG6v_AAE7Jm9J6Iq-pkfBs2L6ozZlTRriRxoMN1aUUyKDN4NpuH_Xxwj5Db0rjXvGLVdVlyUQBB8KZ8YEeRo9XyKnMJd4Fkly2mMViAQLt5bSG2Oi1Wb9rr7qyfnlAJiBJxxOGZ1doviobJmBzbJoby0lwzhERo8PtfGo993jh1HyS1vuK3e_B71C7zCTXcDd-1zrQkz1WQ6NhRhx7_EMd98i4y0f1tZx4ZolAaNFobh4K9fMzSNN92v16eESWRypsTen-cduMGs7EB9McHRczTaMlRucbXuTRLa6YA')

# Valid JWT Token for Producer
Producer = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MmNiMmQ3YTQxODE0Njc1YTU5MDQ5OTUiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3Nzg3ODk1LCJleHAiOjE2NTc4NzQyOTUsImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.r5WfrQiCt2XKxc8Fxj4tjYQ5fFqmAf8W_e7jbRDK_VSXwlUxuPzsUdTFIQd-w3NynuhpXwSGdjdHgoUdzigCZNmIc6cjV1gNB1bJdf_bZ7XADsKEwyp9Hqwx6XVW_0B3GCDsDfg3tXYULfuWESkLJ2CULdcUGufV26dEeKVsQEw8g8b2InZWD2VkLfkmGzj-skxFM1_JpYBQ5Hlqpm0u8PzMoyqmmaGXmTMXT6Qza_E1wiUJZHK5-WS9cB5EMSFI1wZmx7OpCg2k5qkaxU0K8eWpWPAivVPQsxeXYsy45tAciIFtpnGFCyVgfdxh8fmKG7O-4qdHA_T6tvaFCq_dFQ')

class CastingAgencyTest(unittest.TestCase):
    # Test cases for Casting Agency"""
    # db_drop_and_create_all()
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.test_movie = {
            'title': 'John Wick Chapter 4',
            'release_date': '23/03/2023'
        }

        setup_db(self.app, database_path)
    
    def tearDown(self):
        pass

    #Select all movies from the table """
    def test_get_all_movies(self):
        response = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {Assistant}'}
        )
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    #Select a specific movie id 1 from the table """
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + Assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Home Alone')

    # tests by selecting data by a specific movie using invalid id """
    def test_404_get_movie_by_id(self):
        response = self.client().get(
            '/movies/444',
            headers={"Authorization": "Bearer " + Assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

     #tests RBAC for updating a movie
    def test_403_patch_movie_unauthorized(self):
        response = self.client().patch(
            '/movies/2',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {Assistant}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')
     
     #tests RBAC for updating a movie using invalid token
    def test_401_patch_movie_invalidtoken(self):
        response = self.client().patch(
            '/movies/2',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {Assistant_invalid}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'invalid_token')
        self.assertEqual(data['description'], 'Access denied due to invalid token')

    # tests RBAC for deleting a movie
    def test_403_delete_movie(self):
        response = self.client().delete(
            '/movies/3',
            headers={'Authorization': f'Bearer {Assistant}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

     #  Tests to get all actors
    def test_get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {Assistant}'}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Test to get a specific actor
    def test_get_actor_by_id(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + Assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'John')

    # tests for getting unavailable actor
    def test_404_get_actor_by_id(self):
        response = self.client().get(
            '/actors/999',
            headers={"Authorization": "Bearer " + Assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests RBAC for updating an actor by Assistant Role
    def test_403_patch_actor_unauthorized(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'Will Smith', 'age': 49, "gender": "male"},
            headers={'Authorization': f'Bearer {Assistant}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests RBAC for deleting an actor
    def test_403_delete_actor(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {Assistant}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # test RBAC for Director 
    #tests RBAC for creating a movie using valid token
    def test_403_post_movie_unauthorized(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {Director}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')
    
    #  Director
    #tests RBAC for creating a movie using invalid token
    def test_401_post_movie_invalidtoken(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {Director_invalid}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'invalid_token')
        self.assertEqual(data['description'], 'Access denied due to invalid token')

    # Producer
    # Test to create a movie
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json={'title':'John Wick Chapter 4', 'release_date': "23/03/2023"},
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'John Wick Chapter 4')
        self.assertEqual(
            data['movie']['release_date'],
            'Wed, 22 Mar 2023 18:30:00 GMT'
        )

    # Test to create a movie without request body
    def test_400_post_movie(self):
        response = self.client().post(
            '/movies',
            json={},
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # Test to Update a movie
    def test_patch_movie(self):
        response = self.client().patch(
            '/movies/3',
            json={'title': 'Operation Fortune', 'release_date': "Sun, 25 Dec 2022 03:00:00 GMT"},
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Operation Fortune')
        self.assertEqual(
            data['movie']['release_date'],
            'Sat, 24 Dec 2022 21:30:00 GMT'
        )
    
    # Test that 400 is returned if no data is sent to update a movie
    def test_400_patch_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={},
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests that 404 is returned for updating unavilable movie
    def test_404_patch_movie(self):
        response = self.client().patch(
            '/movies/999',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # test to delete a movie 
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/4',
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])
    
    # tests to delete a unavailable movie
    def test_404_delete_movie(self):
        response = self.client().delete(
            '/movies/555',
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create an actor
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Tom Cruise', 'age': 40, "gender": "Male"},
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Tom Cruise')
        self.assertEqual(data['actor']['age'], 40)
        self.assertEqual(data['actor']['gender'], 'Male')

    # Test to Update an actor
    def test_patch_actor(self):
        response = self.client().patch(
            '/actors/4',
            json={'name': 'Halle Berry', 'age': 35, "gender": "Female"},
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Halle Berry')
        self.assertEqual(data['actor']['age'], 35)
        self.assertEqual(data['actor']['gender'], 'Female')

    # Test that 400 is returned if no data is sent to update an actor
    def test_400_patch_actor(self):
        response = self.client().patch(
            '/actors/4',
            json={},
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # Test to verify 400 while creating an actor if no data is sent
    def test_400_post_actor(self):
        response = self.client().post(
            '/actors',
            json={},
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests that 404 is returned for an invalid id to get a specific actor
    def test_404_patch_actor(self):
        response = self.client().patch(
            '/actor/635',
            json={'name': 'Tom Hanks', 'age': 45, "gender": "male"},
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # test to delete an actor 
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/5',
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # test for deleting an invalid actor
    def test_404_delete_actor(self):
        response = self.client().delete(
            '/actors/555',
            headers={'Authorization': f'Bearer {Producer}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

# Make the tests executable
if __name__ == "__main__":
    unittest.main()