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
        assert app.getTimestamp() == expected


    def test_getLeaderboard(self):
        expected = {"message" : "Database is empty"}
        assert app.getLeaderBoard() == expected


    def test_sortListFunction(self):
        expected = 0
        assert app.sortListFunction({'rank' : 0}) == expected


    def test_getLeaderBoardWithCountryIsoCode(self):
        expected = {"message": "Database is empty"}
        assert app.getLeaderBoard() == expected


    def test_parse_json(self):
        expected = {'test':'test'}
        assert app.parse_json({'test': 'test'}) == expected


    def test_getUserProfileWithGuid(self):
        expected = None
        assert app.getUserProfileWithGuid("some-UUID-input") == expected


    def test_landingPage(self):
        expected = "The resource cannot be found"
        assert app.landingPage() == expected


    def test_leaderboardPage(self):
        api_url = "http://localhost:3000"
        leaderboard_url = "{}/leaderboard".format(api_url)
        expected = {"message": "Database is empty"}
        response = requests.get(leaderboard_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())
        #assert json.loads(app.leaderboardPage()) == expected


    def test_leaderboardPageWithCountryIsoCode(self):
        api_url = "http://localhost:3000"
        leaderboard_url = "{}/leaderboard/tr".format(api_url)
        expected = {"message": "Database is empty"}
        response = requests.get(leaderboard_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.json())
        # assert json.loads(app.leaderboardPage()) == expected


    def test_userprofilePageWithGuid(self):
        pass

if __name__ == '__main__':
    unittest.main()