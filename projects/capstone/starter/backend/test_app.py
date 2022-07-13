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
Assistant = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Mjg5MDMyMzk2MWM5ZDAwNjhhMjQxMDgiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3NjYzNTIzLCJleHAiOjE2NTc3NDk5MjMsImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.OwcuzgWuC70dwJ_6GXKu7KEw9FvIDYUgB2FuAG3QlWqpBKFxGnR5v76PWeNqk0gaE8F5KzuZ2VeNkeT7YZNwkctie_HzhqDn1JsQNFN262q2jdJ6ek8WGDXtIVf-txU64J1FBbUprcGRXms9Oe1Xn7kW2MTDjJdMB3LlPQ0xq1CF0kSxsIXhLyJJnwIXC73U-OqNYs7ifE1qlKEb8FBg_LwiBaNAoqD35o1bg9AeGikMbdJUqusXiqvhG9NeFtAG6ijN7eqxGknR0uCPxvJSa1z1YuKXwDBVZC7epj6DKOgXaKmk_4m76W6G0quTOk6SupjN9S7UUfFEj0ns3O0F-Q')
# Expired / Invalid JWT Token for Assistant 
Assistant_invalid = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Mjg5MDMyMzk2MWM5ZDAwNjhhMjQxMDgiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3NTA3MjgxLCJleHAiOjE2NTc1MjUyODEsImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.YfQWrTS26u3Bqnr-jQJb59EIB8V3WcZHaabW9XDB7lsMPa7X8jMg-Q9P9atcVJNZRjDL9mjqvy6bipBqYWmPYGaLI2QkNI05MuzNYdezgZiUaLQrvXm6_LO7DNn2dKzu6hzeQEdkTQ7eI6-piKozcHkt9trgKSDlqcEBms-syRr6_5HhmX_Yh9Q4ygbjLkGI-eKuXcYhmVIWj1N1dCfquxput4n-l4Srg_OCv2d2EQ4YU4rlgrPCbdwkLgohvigoUW02YurLNR86QWhyF-KlAwKtmUjN1cpfTsCdLuGzgEpZRNr4xQeG2qKWYuaAV9MMLrqWJTYuNgl2_YXrfolqOg')

# Valid JWT Token for Director
Director = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Mjg5MDJjZGQxZWI2ZjAwNjhkMTljNzkiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3NjYzNjIxLCJleHAiOjE2NTc3NTAwMjEsImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.cTSr_h2I4dnZk0VyaDn7ZW92rS8_jolgFGQPhj742qCgwyBzTci_5HeLOyMQ5JwMqBLZFniSEBKPxGYWyaZHNcd0oPSDcRXuHB8RazeVlJARRNjKj4Kb99oilmxa7q4OHABHsnW3cR1WheOg8RROvCi14ZVNFhVP0wBSyRoqD7XxTw1XFqRxSUyqkfBl5cYlmviO5UFQKV8eV0hUzYhDNY9VZbXWEjYwy2OIYxuFIc4onhecrCrzMVZagltJ2r74MoRSiE8i-jp5_UNekMp8FvhKbFdKTM6tol7u-3DoWPQ5yBasu5X4vyMgsOHzFtE8ntEPueQRa3AVx95fdlsfUQ')
# Expired / Invalid JWT Token for Director
Director_invalid = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Mjg5MDJjZGQxZWI2ZjAwNjhkMTljNzkiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3NDg1MzY5LCJleHAiOjE2NTc1MDMzNjksImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.g2eaQN_wXKL-1rfWND9RB0V-Bvp-TlsnNxWbG5OIkn-9OOcqG6v_AAE7Jm9J6Iq-pkfBs2L6ozZlTRriRxoMN1aUUyKDN4NpuH_Xxwj5Db0rjXvGLVdVlyUQBB8KZ8YEeRo9XyKnMJd4Fkly2mMViAQLt5bSG2Oi1Wb9rr7qyfnlAJiBJxxOGZ1doviobJmBzbJoby0lwzhERo8PtfGo993jh1HyS1vuK3e_B71C7zCTXcDd-1zrQkz1WQ6NhRhx7_EMd98i4y0f1tZx4ZolAaNFobh4K9fMzSNN92v16eESWRypsTen-cduMGs7EB9McHRczTaMlRucbXuTRLa6YA')

# Valid JWT Token for Producer
Producer = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MmNiMmQ3YTQxODE0Njc1YTU5MDQ5OTUiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3NjYzNzYyLCJleHAiOjE2NTc3NTAxNjIsImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.YXmwwOLCcMB0FB_f9GK-C0rXGqwcvYTMMxjv7-WHmpVmPQzkGU4RhelDOOXI3fmftMeEsRSW3CNF9VUwyfzJVL6l7IQ4abJ6pNtW1W5S0QlRCT1ipH6RMXdymvr8qc-1DmyG9NTOPzeKsJsYNBpf0iLJu7dRUjDM7GINjXSBYENqe5eMPAUdFWLiHDTDlCaXb3mAvu2-hxwLyU0cg9U7UvhS8UQ9NGZuEZqNa0alVmSEnE-bGHvegcYQUCOcs91KnrGb9Myb9jsr8f5vTpgE-aIa0jyQxIh0RNLxW3GuhoHi4YP_f4A4SEXrk1RFX5gXTBeGmC13_iJEHzR8Gx__-w')

class CastingAgencyTest(unittest.TestCase):
    """Test cases for Casting Agency""
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

    """Select all movies from the table """
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

    """ Select a specific movie id 34 from the table """
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/34',
            headers={"Authorization": "Bearer " + Assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Home Alone')

    """ tests by selecting data by a specific movie using invalid id """
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
            '/movies/35',
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
            '/movies/35',
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
            '/movies/40',
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
            '/actors/44',
            headers={"Authorization": "Bearer " + Assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Diana')

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
            '/actors/41',
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
            '/actors/41',
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
            '/movies/36',
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
            '/movies/37',
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
            '/movies/45',
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
            '/actors/39',
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
            '/actors/39',
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
            '/actors/47',
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