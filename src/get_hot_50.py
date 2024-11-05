import sys
import praw
import json
from datetime import datetime
import os

import praw.models

def main(args):
    reddit = praw.Reddit("scraper", user_agent="ubuntu:nlp-project:v1.0.0.0 (by u/calebkbradford1)")
    for subreddit_string in args:
        to_dump = {}
        for submission in reddit.subreddit(subreddit_string).hot(limit=50):
            comments = []
            if submission.stickied:
                continue
            current_submission = {}
            current_submission['title'] = submission.title
            current_submission['text'] = submission.selftext
            for comment in submission.comments.list():
                if type(comment) != praw.models.Comment:
                    continue
                comments.append(comment.body)
            current_submission['comments'] = comments
            to_dump[submission.id] = current_submission
        
        now = datetime.now()
        date_string = now.strftime("%m_%d_%H:%M")
        if not os.path.exists(f"data/{subreddit_string}"):
            os.makedirs(f"data/{subreddit_string}")
        with open(f"data/{subreddit_string}/{date_string}.json", 'w') as writer:
            json.dump(to_dump, writer, indent=3)
        
    


if __name__ == "__main__":
    main(sys.argv[1:])