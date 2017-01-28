import praw
import datetime
import os
import re
import nltk
from time import sleep
from configparser import ConfigParser


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
    print('Could-of-bot 0.2 by u/DukeHarris')
    print("================================")

    # Check for config file
    if not os.path.exists('config.ini'):
        print('No config file.')
        sys.exit()

    config = ConfigParser()
    config.read('config.ini')

    reddit = praw.Reddit(
        user_agent = 'Could-of-bot 0.2 by u/DukeHarris see '
                'https://github.com/DukeHarris/could-of-bot',
        username = config['reddit']['user'],
        password = config['reddit']['password'],
        client_id = config['reddit']['client_id'],
        client_secret = config['reddit']['client_secret']
    )

    # also match the next word for NL analysis
    pattern = re.compile(r".*\b(could|should|would)\s*of\b\s*(\b\w+\b)?")
    running = True
    while running:
        try:

            comments = reddit.subreddit('all').stream.comments()

            for comment in comments:
                if  comment.author is not None and \
                    comment.author.name.lower() != config['reddit']['user'] and \
                    comment.id not in replied_to:

                    match = pattern.match(comment.body.lower())
                    if match:
                        if len(match.groups()) == 1:
                            reply_to(comment, match.groups()[0])
                        else:
                            # build a sentence for nltk
                            testString = "I {} have {}".format(match.groups()[0], match.groups()[1])
                            text = nltk.word_tokenize(testString)
                            result = nltk.pos_tag(text)
                            print(testString, result[3][1])
                            # check if the last word is a verb, past participle
                            # or verb, past tense
                            if result[3][1] == "VBN" or if result[3][1] == "VBD":
                                reply_to(comment, match.groups()[0])

        except KeyboardInterrupt:
            running = False
        except Exception as e:
            now = datetime.datetime.now()
            print(now.strftime("%m-%d-%Y %H:%M"))
            print(traceback.format_exc())
            print('[ERROR] ', e)
            sleep(30)
            continue

def reply_to(comment, word):
    print(comment.body.lower())
    comment.reply("It's either {} **HAVE** or {}**'VE**, but never {} **OF**. \n\n See [Grammar Errors](http://www.grammarerrors.com/grammar/could-of-would-of-should-of/) for more information.".format(word, word, word))
    replied_to.add(comment.id)
    with open("replied_to.txt", "a") as f:
        f.write(comment.id + "\n")

# Call main function
main()