export FLASK_DEBUG=True
export ENV='development'
export FLASK_APP=app
#APP DB (HEROKU)
export DATABASE_URL='postgres://sllzleecfdqjec:c6b288f22f662c6e5f0019780d74e81bcffeaca4e6b9f60c11c8608a670800a2@ec2-52-205-61-230.compute-1.amazonaws.com:5432/d9ooihivh7csbs'
#AUTH0 Details
export AUTH0_DOMAIN = 'manifsnd.us.auth0.com'
export ALGORITHMS = ['RS256']
export API_AUDIENCE = 'castingagency'
#JWTs for all 3 users
export ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Mjg5MDMyMzk2MWM5ZDAwNjhhMjQxMDgiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3Nzg3NDA1LCJleHAiOjE2NTc4NzM4MDUsImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.LisjREAAkE4ciGOvVqJs7n4LK4Gj884Jyqq8BzflvWqYZZgiPWixoE2YAZlG9cMeKH1SVDOhQ6Sf9uIxzd3gFRrP9kpVtvNshjpZ0Fm0b09u853_B4Ss4AOqYHUBqf8ubF_SnICUaj2kl7ofUIOpnpVrG7wixry9f6ssLLEPwqgHQA3WOVagyAqk7XDj4KCW67kL2yzP8lQBQv6PnzQzrR8OGdqSeu5uw_-lzPPwKhxE60mPPJCkMNsDKC6zJSGwP_AS3DAwnSjdNnRLpYvXtgpOQbpxo8hyqc7odhcOVgHfYOeiVuZ7JTGknuodhePsmqEs35b38a4FIvRoj0p2ww'
export DIRECTOR  = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Mjg5MDJjZGQxZWI2ZjAwNjhkMTljNzkiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3NjYzNjIxLCJleHAiOjE2NTc3NTAwMjEsImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.cTSr_h2I4dnZk0VyaDn7ZW92rS8_jolgFGQPhj742qCgwyBzTci_5HeLOyMQ5JwMqBLZFniSEBKPxGYWyaZHNcd0oPSDcRXuHB8RazeVlJARRNjKj4Kb99oilmxa7q4OHABHsnW3cR1WheOg8RROvCi14ZVNFhVP0wBSyRoqD7XxTw1XFqRxSUyqkfBl5cYlmviO5UFQKV8eV0hUzYhDNY9VZbXWEjYwy2OIYxuFIc4onhecrCrzMVZagltJ2r74MoRSiE8i-jp5_UNekMp8FvhKbFdKTM6tol7u-3DoWPQ5yBasu5X4vyMgsOHzFtE8ntEPueQRa3AVx95fdlsfUQ'
export PRODUCER  = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRCM2sxeWQwZTkxenZSUDUzVkRadiJ9.eyJpc3MiOiJodHRwczovL21hbmlmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MmNiMmQ3YTQxODE0Njc1YTU5MDQ5OTUiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNjU3Nzg3ODk1LCJleHAiOjE2NTc4NzQyOTUsImF6cCI6IjI2RzFSejZqTVpvRlZjb0FGd1JBdUtYUGxONDlzdGhMIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.r5WfrQiCt2XKxc8Fxj4tjYQ5fFqmAf8W_e7jbRDK_VSXwlUxuPzsUdTFIQd-w3NynuhpXwSGdjdHgoUdzigCZNmIc6cjV1gNB1bJdf_bZ7XADsKEwyp9Hqwx6XVW_0B3GCDsDfg3tXYULfuWESkLJ2CULdcUGufV26dEeKVsQEw8g8b2InZWD2VkLfkmGzj-skxFM1_JpYBQ5Hlqpm0u8PzMoyqmmaGXmTMXT6Qza_E1wiUJZHK5-WS9cB5EMSFI1wZmx7OpCg2k5qkaxU0K8eWpWPAivVPQsxeXYsy45tAciIFtpnGFCyVgfdxh8fmKG7O-4qdHA_T6tvaFCq_dFQ'