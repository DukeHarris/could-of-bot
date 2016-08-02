import praw
import datetime
import os
from time import sleep
from configparser import ConfigParser

reddit = praw.Reddit('Could-of-bot 0.1 by u/DukeHarris see '
                'https://github.com/DukeHarris/could-of-bot')


# Have we run this code before? If not, create an empty list
if not os.path.isfile("replied_to.txt"):
    replied_to = set()
# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("replied_to.txt", "r") as f:
        replied_to = f.read()
        replied_to = replied_to.split("\n")
        replied_to = set(replied_to)

def main():

    print("================================")
    print('Could-of-bot 0.1 by u/DukeHarris')
    print("================================")

    # Check for config file
    if not os.path.exists('config.ini'):
        print('No config file.')
        sys.exit()

    config = ConfigParser()
    config.read('config.ini')

    reddit.login(config['reddit']['user'], config['reddit']['password'], disable_warning=True)


    running = True
    while running:
        try:

            comments = praw.helpers.comment_stream(reddit, "all")

            for comment in comments:
                if  comment.author is not None and \
                    comment.author.name.lower() != config['reddit']['user'] and \
                    comment.id not in replied_to:

                        if "could of " in comment.body.lower():
                            reply_to(comment, "could")
                        elif "should of " in comment.body.lower():
                            reply_to(comment, "should")
                        elif "would of " in comment.body.lower():
                            reply_to(comment, "would")

        except KeyboardInterrupt:
            running = False
        except praw.errors.RateLimitExceeded as e:
            print("[Error] Rate limit exceeded. Sleeping for {}...".format(e.sleep_time))
            sleep(e.sleep_time)
            continue
        except Exception as e:
            now = datetime.datetime.now()
            print(now.strftime("%m-%d-%Y %H:%M"))
            print(traceback.format_exc())
            print('[ERROR] ', e)
            sleep(30)
            continue

def reply_to(comment, word):
    print(comment.id)
    comment.reply("It's {} **HAVE**, not {} **OF**! \n\n See [Grammar Errors](http://www.grammarerrors.com/grammar/could-of-would-of-should-of/) for more information.".format(word, word))
    replied_to.add(comment.id)
    with open("replied_to.txt", "a") as f:
        f.write(comment.id + "\n")

# Call main function
main()