import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

ACCESS_TOKEN = "4870715640.a48e759.874aba351e5147eca8a9d36b9688f494"
BASE_URL = "https://api.instagram.com/v1/"

#instabot 1.0#
def self_info():
    """
    This function gets the info of self according to access token.
    1.Make URL
    2.Make request
    """
    url = (BASE_URL + "users/self/?access_token=%s") % (ACCESS_TOKEN)
    user_info = requests.get(url).json()
    if user_info["meta"]["code"] == 200:
        print "******user details are:******"
        print ("Instagram username:%s") % user_info["data"]["username"]
        print ("Followers count :%s") % user_info["data"]["counts"]["followed_by"]
        print ("Following count=%s") % user_info["data"]["counts"]["follows"]
        print("No. of media=%s") % user_info["data"]["counts"]["media"]
    else:
        print"Something went wrong!"


def get_user_id(instagram_username):
    """
        to get user id of other instagram user
        1.Make the URL
        2.Make the request
     """
    url = (BASE_URL + "users/search?q=%s&access_token=%s") % (instagram_username, ACCESS_TOKEN)
    user_id = requests.get(url).json()
    if user_id["meta"]["code"] == 200:
        return user_id["data"][0]["id"]
    else:
        print "Something went wrong!"


def get_user_info(instagram_username):
    """
        Gives instagram name,followers count,following count and no. of posts
        1.Get the user id
        2.Make the URL
        3.Make the request
    """
    user_id = get_user_id(instagram_username)
    if user_id == None:
        print "User not found!!"
    else:
        url = (BASE_URL + "users/%s?access_token=%s") % (user_id, ACCESS_TOKEN)
        user_info =  requests.get(url).json()
        if user_info["meta"]["code"] == 200:
            print "******user details are:******"
            print ("Instagram username:%s") % user_info["data"]["username"]
            print ("Followers count :%s") % user_info["data"]["counts"]["followed_by"]
            print ("Following count=%s") % user_info["data"]["counts"]["follows"]
            print("No. of media=%s") % user_info["data"]["counts"]["media"]
        else:
            print "Something went wrong!"


def download_image(image_url, image_name):
    return urllib.urlretrieve(image_url, image_name)

def get_own_post():
    """
    Get own post .
    It also gives option for downloading
    1.Make the url
    2.Make the request
    """
    url = (BASE_URL + "users/self/media/recent/?access_token=%s") % ACCESS_TOKEN
    own_media =  requests.get(url).json()
    if own_media["meta"]["code"] == 200:
        data = own_media["data"]
        images = []
        print "*****image name and respective  url are :****"
        for e in data:
            images.append({"url": e["images"]["standard_resolution"]["url"], "name": e["id"] + ".jpeg"})
        for d in range(0, len(images)):
            print ("Name:%s\nURL:%s") % (images[d]["name"], images[d]["url"])
        ans = raw_input("do you wish to download?y/n?")
        if (ans == 'y') or (ans == 'Y'):
            for e in range(0, len(images)):
                download_image(images[e]["url"], images[e]["name"])
            print "Images downloaded!"
    else:
        print "Something went wrong!"


def get_user_post(instagram_username):
    """
        get other user's special image or all the images with their name along with URL .
        option for downloading
        1.Get the user id
        2.Make the url
        3.Make the request
    """
    user_id = get_user_id(instagram_username)
    if user_id == None:
        print "User not found!!"
    else:
        url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id, ACCESS_TOKEN)
        user_media =  requests.get(url).json()
        if user_media["meta"]["code"] == 200:
            data = user_media["data"]
            images = []
            likes = []
            print "*****all the image name and respective url are :****"
            for e in data:
                images.append({"url": e["images"]["standard_resolution"]["url"], "name": e["id"] + ".jpeg"})
                likes.append({"url": e["images"]["standard_resolution"]["url"], "name": e["id"] + ".jpeg",
                              "likes": e["likes"]["count"]})
            option = raw_input("Do you want to get some special picture with MINIMUM likes or ALL the pictures?for special picture press y:")
            if (option == "y"):
                min_like = likes[0]["likes"]
                for l in range(0, len(likes)):
                    if (likes[l]["likes"] < min_like):
                        min_like = (likes[l]["likes"])
                        min_index = l
                print ("Name:%s\nURL:%s\nLikes:%s") % (
                likes[min_index]["name"], likes[min_index]["url"], likes[min_index]["likes"])
                ans = raw_input("do you wish to download?y/n?")
                if (ans == 'y') or (ans == 'Y'):
                    download_image(likes[min_index]["url"], likes[min_index]["name"])
                    print "Images downloaded!"
            else:
                for d in range(0, len(images)):
                    print ("Name:%s\nURL:%s") % (images[d]["name"], images[d]["url"])
                ans = raw_input("do you wish to download?y/n?")
                if (ans == 'y') or (ans == 'Y'):
                    for e in range(0, len(images)):
                        download_image(images[e]["url"], images[e]["name"])
                    print "Images downloaded!"
        else:
            print "Something went wrong!"


def get_media_id(instagram_username):
    """
        This function helps to get the media id instagram user's recent post
        1.Get the user id
        2.Make the URL
        3.Make the request

    """
    user_id = get_user_id(instagram_username)
    if user_id == None:
        print "User not found!!"
        exit()
    url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id, ACCESS_TOKEN)
    user_media =  requests.get(url).json()
    if user_media["meta"]["code"] == 200:
        media_id = user_media["data"][0]["id"]
        return media_id
    else:
        print "Something went wrong!"


def like_a_post(instagram_username):
    """
            To like instagram user's recent post
            1.Get the media id
            2.Make the URL
            3.Make the request

    """
    media_id = get_media_id(instagram_username)
    url = BASE_URL + "media/%s/likes" % (media_id)
    parameter = {"access_token": ACCESS_TOKEN}
    post_request = requests.post(url, parameter).json()
    if post_request['meta']['code'] == 200:
        print "Like was successful!"
    else:
        print "Something went wrong!"


def post_liked():
    """
            This function helps to get the list of posts liked by access token holder
            1.Make the URL
            2.Make the request

    """
    url = (BASE_URL + "users/self/media/liked?access_token=%s") % (ACCESS_TOKEN)
    media_liked =  requests.get(url).json()
    if media_liked["meta"]["code"] == 200:
        medias = [media_liked["data"][x]["id"] for x in range(0, len(media_liked["data"]))]
    print ("**Here are the media id's of post liked by you**")
    for i in range(0, len(medias)):
        print medias[i]


def make_comments(instagram_username):
    """
            This function helps to make comments on  instagram user's recent post
            1.Get the user id
            2.Make the URL for media information
            3.Make the request
            4.Get media id
            5.Make the URL  for making comments
            6.Make the request

    """
    user_id = get_user_id(instagram_username)
    if user_id == None:
        print "User not found!!"
        exit()
    request_url = BASE_URL + "users/%s/media/recent/?access_token=%s" % (user_id, ACCESS_TOKEN)
    media_info = requests.get(request_url).json()
    if media_info['meta']['code'] == 200:
        media_id = media_info["data"][0]["id"]
        url = BASE_URL + "media/%s/comments" % (media_id)
        comment = raw_input("what comment do you want to make?")
        parameter = {"access_token": ACCESS_TOKEN, "text": comment}
        post_request = requests.post(url, parameter).json()
        if post_request['meta']['code'] == 200:
            print "comment was successful!"
        else:
            print "Something went wrong!"
    else:
        print "Something went wrong!"


def view_comments(instagram_username):
    """
                This function helps to view comments on  instagram user's recent post
                1.Get the user id
                2.Make the URL for media information
                3.Make the request
                4.Get media id
                5.Make the URL for viewing comments
                6.Make the request

    """

    user_id = get_user_id(instagram_username)
    if user_id == None:
        print "User not found!!"
        exit()
    request_url = BASE_URL + "users/%s/media/recent/?access_token=%s" % (user_id, ACCESS_TOKEN)
    media_info = requests.get(request_url).json()
    if media_info['meta']['code'] == 200:
        media_id = media_info["data"][0]["id"]
        url = BASE_URL + "media/%s/comments?access_token=%s" % (media_id, ACCESS_TOKEN)
        get_request = requests.get(url).json()
        if get_request['meta']['code'] == 200:
            comments = [get_request["data"][x]["text"] for x in range(0, len(get_request["data"]))]
        else:
            print "Something went wrong in viewing comment!"
            exit()
        print "**comments on the post are**"
        for i in range(0, len(comments)):
            print comments[i]
    else:
        print "Something went wrong in accesing media id!"


def delete_negative_comment(instagram_username):
    """
                This function helps to delete negative comments on  instagram user's recent post
                1.Get the media id
                2.Make the URL
                3.Make the request
                4.Use NaiveBayesAnalyser and find negative comments
                5.Make the URL for deleting
                6.Make the request

        """
    media_id = get_media_id(instagram_username)
    url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    comment_info = requests.get(url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info["data"])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    print "Negative comment:%s" % comment_text
                    delete_url =(BASE_URL + "media/%s/comments/%s?access_token=%s")%(media_id,comment_id,ACCESS_TOKEN)
                    delete_info = requests.delete(delete_url).json()
                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print "positive comment:%s" % comment_text
        else:
            print "No comments!"
    else:
        print "Something went wrong!"


def climate_check(latitude, longitude):
    """
    To get images in a parrticular geographical zone and through their caption analyses if it's a natural calamity.
    1.Make the URL for location information
    2.Make the request
    3.Get media id
    4.Analyse captions
    5.Check for calamity
    """
    url = (BASE_URL + "locations/search?lat=%s&lng=%s&access_token=%s") % (latitude, longitude, ACCESS_TOKEN)
    location_info = requests.get(url).json()
    if location_info['meta']['code'] == 200:

        location_id = [location_info["data"][x]["id"] for x in range(0, len(location_info["data"]))]

        media_list = []

        for i in range(0, len(location_id)):
            request_url = (BASE_URL + "locations/%s/media/recent?access_token=%s") % (location_id[i], ACCESS_TOKEN)
            media_request = requests.get(request_url).json()
            if media_request["meta"]["code"] == 200:
                media_list.append(media_request["data"])
            else:
                print "Code other than 200"
                exit()

        media_info = [media_list[y] for y in range(0, len(media_list))]

        caption = [media_info[j][e]["caption"]["text"] for j in range(0, len(media_info)) if len(media_info[j]) > 0 for
                   e in range(0, len(media_info[j]))]
        for m in range(0, len(caption)):
            print ">> %s " % caption[m]
        if len(caption):
            print "***Images with these captions found!***"
        else:
            print "***Woops!No images in this area***"

        calamities = ["Avalanche", "avalanche", "Landslide", "Landslide", "Hailstorm", "hailstorm", "Heatwave",
                      "heatwave", "Cloudburst", "cloudburst", "Earthquake", "earthquake", "Flood", "flood", "Cyclone",
                      "cyclone", "Tsunami", "tsunami", "Drought", "drought", "Thunderstorm", "thunderstorm", "Blizzard",
                      "blizzard", "Volcano", "volcano"]
        check = False

        for k in range(0, len(caption)):
            for l in range(0, len(calamities)):
                if calamities[l] in caption[k]:
                    check = True
                    break
            if check:
                print "This picture with caption :%s ->  denotes a calamity of: %s" % (caption[k], calamities[l])
            else:
                print "This picture with caption :%s ->  denotes no calamity" % (caption[k])
    else:
        print "Something went wrong!"


again = True
print "Hello!!! Welcome to InstaBot :)!"
while again:
    print "\n"
    print"What would you like to do?"
    print "Menu options:"
    print "********************************"
    print "1.Get your own details"
    print "2.Get user id of a user by username"
    print "3.Get instagram account details of a user by username"
    print "4.Get your own post"
    print "5.Get the  posts of a user by username"
    print "6.Get list of recent media liked by you"
    print "7.Like the recent post of a user"
    print "8.View all comments on recent post of a user"
    print "9.Make a comment on the recent post of a user"
    print "10.Delete negative comments from the recent post of a user"
    print "11.Check if any natural calamity in the area by using geographical coordinates"
    print "12.Exit"

    choice = raw_input("Enter you choice: ")
    print "\n"
    if choice == "1":
        self_info()
    elif choice == "2":
        instagram_username = raw_input("Enter the instagram username of the user: ")
        print get_user_id(instagram_username)
    elif choice == "3":
        instagram_username = raw_input("Enter the instagram username of the user: ")
        get_user_info(instagram_username)
    elif choice == "4":
        get_own_post()
    elif choice == "5":
        instagram_username = raw_input("Enter the instagram username of the user: ")
        get_user_post(instagram_username)
    elif choice == "6":
        post_liked()
    elif choice == "7":
        instagram_username = raw_input("Enter the instagram  username of the user: ")
        like_a_post(instagram_username)
    elif choice == "8":
        instagram_username = raw_input("Enter the instagram  username of the user: ")
        view_comments(instagram_username)
    elif choice == "9":
        instagram_username = raw_input("Enter the instagram  username of the user: ")
        make_comments(instagram_username)
    elif choice == "10":
        instagram_username = raw_input("Enter the username of the user: ")
        delete_negative_comment(instagram_username)
    elif choice == "11":
        latitude = raw_input("enter the georgraphical latitude coordinate in decimal:")
        longitude = raw_input("enter the georgraphical longitude coordinate in decimal:")
        climate_check(latitude, longitude)
    elif choice == "12":
        again = False
        exit()
    else:
        print "wrong choice!"


