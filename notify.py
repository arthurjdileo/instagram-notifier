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
    with open(IG_USER+".json","w") as write_file:
        json.dump(followers, write_file)

def checkFollowers(api, user_id):
    unfollowed = set()

    newFollowers = getTotalFollowers(api, user_id)

    with open(IG_USER+".json") as file:
        oldFollowers = json.load(file)


    for f in oldFollowers:
        if f not in newFollowers:
            unfollowed.add(f)

    return unfollowed

def setToStr(s):
    unfollowers = ""
    for element in s:
        unfollowers = unfollowers + element + "\n"
    return unfollowers

if __name__ == "__main__":
    api = InstagramAPI(IG_USER,IG_PASS)
    api.login()

    user_id = api.username_id

    followers = getTotalFollowers(api, user_id)
    unfollowed = checkFollowers(api, user_id)
    if unfollowed != set():
        body =\
        """
%s users have unfollowed you:
        
%s
        """ % (len(unfollowed),setToStr(unfollowed))
        email("Instagram Notifier", SENDTO, "", body, EMAIL_USERNAME, EMAIL_PASS)
    updateFollowers(followers)
