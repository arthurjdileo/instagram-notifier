from InstagramAPI import InstagramAPI
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

IG_USER = ""
IG_PASS = ""
EMAIL_USERNAME = ""
EMAIL_PASS = ""
SENDTO = ""

# email function that uses a from and to address to send an email
def email(sender, receiver, subject, msg, login, pw):
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(msg, "plain"))
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(login,pw)
    text = message.as_string()
    server.sendmail(sender,receiver,text)
    server.quit()

# stores all of the followers usernames into a list
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

# writes + updates json file of the specific user
def updateFollowers(followers):
    with open(IG_USER+".json","w+") as write_file:
        json.dump(followers, write_file)

#compares stored list of followers with updated list to determine unfollowers
def checkFollowers(api, user_id):
    unfollowed = set()

    newFollowers = getTotalFollowers(api, user_id)

    with open(IG_USER+".json") as file:
        oldFollowers = json.load(file)


    for f in oldFollowers:
        if f not in newFollowers:
            unfollowed.add(f)

    return unfollowed

#takes all elements of a set (or similar) and puts it into a multiline string
def setToStr(s):
    unfollowers = ""
    for element in s:
        unfollowers = unfollowers + element + "\n"
    return unfollowers

if __name__ == "__main__":
    #login to instagram account
    api = InstagramAPI(IG_USER,IG_PASS)
    api.login()
    user_id = api.username_id

    #stores list of current followers
    followers = getTotalFollowers(api, user_id)

    #stores list of unfollowed users
    unfollowed = checkFollowers(api, user_id)

    #sends email to client of the users that unfollowed
    if unfollowed != set():
        body =\
        """
%s user(s) have unfollowed you:
        
%s
        """ % (len(unfollowed),setToStr(unfollowed))
        email("Instagram Notifier", SENDTO, "", body, EMAIL_USERNAME, EMAIL_PASS)
        print(str(len(unfollowed)) + " user(s) have unfollowed you. Email sent.")
    else:
        print("Nobody has unfollowed you!")

    #updates local storage of followers with the newly generated list
    updateFollowers(followers)
