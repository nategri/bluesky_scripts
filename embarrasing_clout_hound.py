# comraderobot.bsky.social 's stupid ass embarrasing clout hound script
#
# READEME TYPE STUFF
#
# Requirements:
#  * Python 3.8+
#  * The atproto package ("pip install atproto" will do it)
#
# Note: PLEEEEEEEASE MAKE AN APP PASSWORD FOR THIS DONT USE YR REAL ONE
#


HANDLE = "youraccount.bsky.social"
PASSWORD = "put-an-app-password-here"

import sys
from itertools import islice

from atproto import Client, client_utils

try:
    NUM_ACCOUNTS = int(sys.argv[1])
except:
    print("Type a number after the command to indicate how many accounts you want to list")
    sys.exit(1)

if __name__ == "__main__":
    client = Client()
    profile = client.login(HANDLE, PASSWORD)
    did = profile.did

    api_followers_list = []

    cursor = None

    print("Querying for your followers...", end='')
    while True:
        followers_api = client.get_followers(did, limit=100, cursor=cursor)
        followers = followers_api['followers']
        cursor = followers_api['cursor']
        if not cursor:
            break
        api_followers_list.extend(followers)
        print(".", end='', flush=True)
    print("")

    follower_dict = {x['handle']: {'did': x['did'], 'handle':x['handle']} for x in api_followers_list}

    print("Querying for number of followers your followers have (takes a while)...", end='')
    follower_count_list = []
    iterator = iter(follower_dict.values())
    while api_chunk := list(islice(iterator, 25)):
        did_list = [x['did'] for x in api_chunk]
        profile_api = client.get_profiles(did_list)

        for prof in profile_api.profiles:
            follower_dict[prof.handle]['followers'] = prof.followers_count
        print(".", end='', flush=True)
    print("")

    sorted_followers_list = sorted(follower_dict.values(), key=lambda x: x["followers"])[::-1]

    print("Top {} accounts for account {}, sorted by follower count".format(
        profile.display_name, NUM_ACCOUNTS
    ))
    print("========================================================")
    for i in range(NUM_ACCOUNTS):
        print("{}:    {}".format(sorted_followers_list[i]['handle'], sorted_followers_list[i]['followers']))

