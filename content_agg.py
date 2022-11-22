from abc import ABC, abstractmethod
import praw
import os
from dotenv import load_dotenv

load_dotenv("/home/kali/python_projects/content_aggrigator/Content-Aggregator-1/setup.env")

CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')

print(CLIENT_ID, CLIENT_SECRET)


class Source(ABC):
    ###ABSTRACT CLASS FOR MULTIPLE SITE SOURCES###
    def connect(self):
        pass

    @abstractmethod
    def fetch(self):
        pass


class RedditSource(Source):
    ###REDDIT CONNECTION###

    def connect(self):
        
        self.reddit_con = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, grant_type_access='client_credentials', user_agent='script/1.0') #connection to Reddit API
        return self.reddit_con # Pass Out Connection

class RedditHotProgramming(RedditSource):
    def __init__(self) -> None:
        self.reddit_con = super().connect() # Define reddit_con as super class connect
        self.hot_submissions = []

    def fetch(self, limit: int):
        self.hot_submissions = self.reddit_con.subreddit('programming').hot(limit=limit) # fetch submissions from subreddit with limit to number

    def __repr__(self):
        urls=[]
        for submission in self.hot_submissions: # Append submission to list of urls
            urls.append(vars(submission)['url'])
        return '\n'.join(urls)


class RedditNewPCMasterRace(RedditSource):
    def __init__(self) -> None:
        self.reddit_con = super().connect() # Define reddit_con as super class connect
        self.new_submissions = []
    
    def fetch(self, limit: int):
        self.new_submissions = self.reddit_con.subreddit('pcmasterrace').new(limit=limit) # fetch submissions from subreddit with limit to number
    
    def __repr__(self):
        urls = []
        for submission in self.new_submissions: # Append submission to list of urls
            urls.append(vars(submission)['url'])
        return '\n'.join(urls)

if __name__ == '__main__':
    reddit_top_programming = RedditHotProgramming()
    reddit_top_programming.fetch(limit=10)
    print(reddit_top_programming)

    reddit_new_pcmasterrace = RedditNewPCMasterRace()
    reddit_new_pcmasterrace.fetch(limit=15)
    print(reddit_new_pcmasterrace)