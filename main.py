from pymongo import MongoClient
import json

client = MongoClient()

client = MongoClient("mongodb://localhost:27017")

myDatabase = client['game-x']
myCollection = myDatabase['users']
leaderboard = '{}'

for x in myCollection.find().sort("points", -1).limit(3):
    playingScore = 0
    print(x['user_id'])
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
    leaderboard = x
    for y in agg_result:
        if y['passing_scores'] == 0:
            print("null")
        else:
            print(y['passing_scores'])
        leaderboard['rank'] = y

print(leaderboard)
