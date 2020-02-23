from raven import *
from analyze import *
import argparse

driver = init_driver()
processor = TweetProcessor()

def test(q):
    for tweet in tweet_stream(driver, query_to_url(q), 10):
        data = processor.get_data(tweet)
        print(data.tweet.text)
        print(data.locations)

# NOTE: use argparse because it's easier lol

def main():
    count = 0
    args = []
    while True:
        command = input(" > ").split()
        count = count + 1
        if count > 5:
            print("Do you need help? if so type 'help' ")
            count = 0
        if len(command) > 1:
            if command[0] == "var":
                for i in range(3,len(command)):
                    args.append(i)
        elif len(command) == 1:
            if command[0] == "help":
                print("Help menu--")


if __name__ == '__main__':
    main()
