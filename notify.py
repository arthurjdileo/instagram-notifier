from InstagramAPI import InstagramAPI
import json

def getTotalFollowers(api, user_id):
    followers = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        users = api.LastJson.get('users',[])
        for user in users:
            for key in user:
                if key == "username":
                    followers.append(user[key])
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

def updateFollowers(followers):
    with open("followers.json","w") as write_file:
        json.dump(followers, write_file)

def checkFollowers(api, user_id):
    unfollowed = set()

    newFollowers = getTotalFollowers(api, user_id)

    with open("followers.json") as file:
        oldFollowers = json.load(file)


    for f in oldFollowers:
        if f not in newFollowers:
            unfollowed.add(f)

    return unfollowed


if __name__ == "__main__":
    api = InstagramAPI("USERNAME", "PASSWORD")
    api.login()

    user_id = api.username_id

    followers = getTotalFollowers(api, user_id)
    unfollowed = checkFollowers(api, user_id)
    updateFollowers(followers)
    print(unfollowed)