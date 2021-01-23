import os
import unittest
import time
import app
import json
import requests


class BasicTests(unittest.TestCase):
    ### TESTING ###

    def test_getTimestamp(self):
        expected = int(time.time())
        self.assertEqual(expected, app.getTimestamp())


    def test_getLeaderboard(self):
        expected = {"message" : "Database is empty"}
        self.assertEqual(expected, app.getLeaderBoard())


    def test_sortListFunction(self):
        expected = 0
        self.assertEqual(expected, app.sortListFunction({'rank' : 0}))


    def test_getLeaderBoardWithCountryIsoCode(self):
        expected = {"message" : "Country code is invalid"}
        input = "tr"
        result = app.getLeaderBoardWithCountryIsoCode(input)
        self.assertGreater(len(result), 1)


    def test_getLeaderBoardWithCountryIsoCode(self):
        expected = {"message" : "Country code is invalid"}
        input = "tr"
        result = app.getLeaderBoardWithCountryIsoCode(input)
        self.assertEqual(expected, app.getLeaderBoardWithCountryIsoCode(input))



    def test_parse_json(self):
        expected = {'test':'test'}
        self.assertEqual(expected, app.parse_json({'test': 'test'}))


    def test_getUserProfileWithGuid(self):
        expected = None
        self.assertEqual(expected, app.getUserProfileWithGuid("some-UUID-input"))


    def test_landingPage(self):
        expected = "The resource cannot be found"
        self.assertEqual(expected, app.landingPage())


    def test_leaderboardPage(self):
        api_url = "http://localhost:3000"
        test_url = "{}/leaderboard".format(api_url)
        expected = {"message": "Database is empty"}
        response = requests.get(test_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())
        #assert json.loads(app.leaderboardPage()) == expected


    def test_leaderboardPageWithCountryIsoCode(self):
        api_url = "http://localhost:3000"
        test_url = "{}/leaderboard/tr".format(api_url)
        expected = {"message": "Database is empty"}
        response = requests.get(test_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())


    def test_userprofilePageWithGuid(self):
        api_url = "http://localhost:3000"
        test_url = "{}/user/profile/some-guid".format(api_url)
        expected = {"message": "user doesn't exists"}
        response = requests.get(test_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())


    def test_usercreatePage(self):
        api_url = "http://localhost:3000"
        test_url = "{}/user/create".format(api_url)
        input = {
            "user_id" : "15453e8c-3db5-4dfb-9173-a11016c9b7d11112",
            "display_name" : "samet1111",
            "points" : 0,
            "country" : "tr",
        }
        expected = {}
        response = requests.post(test_url, json=input)
        self.assertEqual(200, response.status_code)


    def test_scoresubmitPage(self):
        api_url = "http://localhost:3000"
        test_url = "{}/score/submit".format(api_url)
        input = {
            "score_worth" : 123,
            "user_id" : "f9501637-963c-44ed-90b1-12800abc1e5f"
        }
        expected = {"message" : "user is not found"}
        response = requests.post(test_url, json=input)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())


    def test_createFakeFieldsPage(self):
        api_url = "http://localhost:3000"
        test_url = "{}/createfields/".format(api_url)
        expected = {
            "message": "fake resources has been inserted",
        }
        response = requests.get(test_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())


    def test_not_found(self):
        api_url = "http://localhost:3000"
        test_url = "{}/some/url/doesnt/exist".format(api_url)
        expected = {"message":"The resource cannot be found"}
        response = requests.get(test_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())


if __name__ == '__main__':
    unittest.main()