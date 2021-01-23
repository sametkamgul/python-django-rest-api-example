from bson import json_util
from flask import Flask, jsonify, request
from pymongo import MongoClient
import json
import time
import names
import random
import uuid

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")

myDatabase = client['game-x']
myCollection = myDatabase['users']


# this returns the 1.2.3 players with their ranks
def getLeaderBoard():
    leaderboard = []
    myFind = {}
    myFilter = {"_id": 0, "points": 1, "display_name": 1, "country": 1, "timestamp":1}
    for x in myCollection.find(myFind, myFilter).sort("points", -1).limit(10):
        # print(x['user_id'])
        playerScore = x["points"]
        playerTimeStamp = x["timestamp"]
        b = myCollection.find({"points": {"$gt": playerScore}}).count()
        c = myCollection.find({"points": {"$eq": playerScore}, "timestamp": {"$lt": playerTimeStamp}}).count()
        x['rank'] = b+c + 1
        leaderboard.append(x)
    leaderboard.sort(key=sortListFunction)
    return leaderboard

# this returns for sorting leaderboard list by rank and presenting in sorted
def sortListFunction(e):
    return e["rank"]

# this returns the 1.2.3 players with their ranks by country iso code(country spesific data)
def getLeaderBoardWithCountryIsoCode(country_iso_code):
    leaderboardWithCountryIsoCode = []
    myFind = {"country": country_iso_code}
    myFilter = {"_id": 0, "points": 1, "display_name": 1, "country": 1}
    for x in myCollection.find(myFind, myFilter).sort("points", -1).limit(3):
        agg_result = myCollection.aggregate(
            [
                {
                    "$match": {
                        "points": {
                            "$gte": x['points']
                        }
                    }
                },
                {
                    "$count": "passing_scores"
                }
            ]
        )
        for a in agg_result:
            print(a)
            x['rank'] = a['passing_scores']
        leaderboardWithCountryIsoCode.append(x)
    return leaderboardWithCountryIsoCode


def parse_json(data):
    return json.loads(json_util.dumps(data))


# this returns user profile finding by GUID and adds its rank
def getUserProfileWithGuid(guid):
    myFind = {"user_id": guid}
    myFilter = {"_id": 0, "points": 1, "display_name": 1, "country": 1}
    userprofileWithGuid = myCollection.find_one(myFind, myFilter)
    print(userprofileWithGuid)
    if userprofileWithGuid is not None:
        agg_result = myCollection.aggregate(
            [
                {
                    "$match": {
                        "points": {
                            "$gte": userprofileWithGuid['points']
                        }
                    }
                },
                {
                    "$count": "passing_scores"
                }
            ]
        )
        for a in agg_result:
            userprofileWithGuid['rank'] = a['passing_scores']
    else:
        pass
    return userprofileWithGuid



# this returns a epoch time in the type of int
def getTimestamp():
    return int(time.time())


@app.route('/', methods=['GET'])
def landingPage():
    return "The resource cannot be found"


@app.route('/leaderboard', methods=['GET'])
def leaderboardPage():
    return jsonify(parse_json(getLeaderBoard()))


@app.route('/leaderboard/<country_iso_code>', methods=['GET'])
def leaderboardPageWithCountryIsoCode(country_iso_code):
    print(country_iso_code)
    return jsonify(parse_json(getLeaderBoardWithCountryIsoCode(country_iso_code)))


@app.route('/user/profile/<guid>', methods=['GET'])
def userprofilePageWithGuid(guid):
    result = getUserProfileWithGuid(guid)
    if result is not None:
        return jsonify(parse_json(result))
    else:
        return jsonify(parse_json({"message" : "user doesn't exists", "success" : False}))


@app.route('/user/create', methods=['POST'])
def usercreatePage():
    # checking the existing guid for preventing collusion
    guid = request.get_json()['user_id']
    myFind = {"user_id": guid}
    myFilter = {"_id": 0, "points": 1, "display_name": 1, "country": 1}
    userprofileWithGuid = myCollection.find_one(myFind, myFilter)
    if userprofileWithGuid is None:
        newUserProfile = {}
        newUserProfile['display_name'] = request.get_json()['display_name']
        newUserProfile['user_id'] = request.get_json()['user_id']
        newUserProfile['points'] = request.get_json()['points']
        newUserProfile['country'] = request.get_json()['country']
        newUserProfile['timestamp'] = getTimestamp()
        print(newUserProfile)
        myCollection.insert(newUserProfile)
        return jsonify(parse_json(newUserProfile))
    else:
        return jsonify(parse_json({"message" : "user exists", "success" : False}))


@app.route('/score/submit', methods=['POST'])
def scoresubmitPage():
    print(request.get_json())
    guid = request.get_json()['user_id']
    scoreWorth = request.get_json()['score_worth']
    myFind = {"user_id": guid}
    myFilter = {"_id": 0, "points": 1, "user_id": 1, "display_name": 1}
    userprofileWithGuid = myCollection.find_one(myFind, myFilter)
    userprofileWithGuid['points'] += scoreWorth     # increase player score
    print(userprofileWithGuid)
    myQuery = {"user_id" : userprofileWithGuid["user_id"]}
    myNewValues = {"$set": {"points" : userprofileWithGuid['points'], "timestamp" : int(time.time())}}
    myCollection.update_one(myQuery, myNewValues)

    # find user rank
    agg_result = myCollection.aggregate(
        [
            {
                "$match": {
                    "points": {
                        "$gte": userprofileWithGuid['points']
                    }
                }
            },
            {
                "$count": "passing_scores"
            }
        ]
    )
    for a in agg_result:
        userprofileWithGuid['rank'] = a['passing_scores']
    return jsonify(parse_json(userprofileWithGuid))


@app.route('/createfields')
@app.route('/createfields/<iteration>')
def createFieldsPage(iteration):
    """
    this function creates fake fields for testing the Restful API
    sample MongoDB field in JSON
    {
        "_id": {
            "$oid": "600887737718091954842845"
        },
        "user_id": "d28d919b-1f95-4003-a2cf-7ede28279d08",
        "display_name": "Hugh Dach V",
        "points": 875,
        "country": "tr",
        "timestamp": 1611171699
    }
    :param iteration:
    :return:
    """

    # null check for iteration
    if iteration is None:
        iteration = 5
    else:
        iteration = int(iteration)

    countryCodeList = ["tr", "en", "de", "es", "it"]
    for x in range(iteration):
        newField = {
            "user_id": str(uuid.uuid4()),
            "display_name": names.get_full_name().replace(' ', ''),
            "points": random.randint(0, 9999),
            "country": countryCodeList[random.randint(0, len(countryCodeList) - 1)],
            "timestamp": int(time.time())
        }
        myCollection.insert(newField)
        time.sleep(1)
        print("inserted:", newField)
    return jsonify(parse_json({"message" : str(iteration) + " amount of resource(s) has been entered", "success": True}))


@app.errorhandler(404)
def not_found(*args):
    """Page not found."""
    return jsonify(parse_json({"message":"The resource cannot be found"}))


if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)
