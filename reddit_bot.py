import praw
import random

class bot_reach:
    
    def __init__(self):
        self.reddit = praw.Reddit(client_id = 'fJqbl_xNWAriWw',
                     client_secret = 'hI8yqCuGpd0IYSzZ3SS6_XWfjys',
                     user_agent = 'personal use_script')
        
    def populate_upvotes(self, user):
        user = self.reddit.redditor(user)
        
        #num can be limited with user.upvoted(limit= #)
        #after upvotes have become many
        upvotes = user.upvoted()
        
        for u in upvotes:
            str_subreddit = str(u.subreddit)
            str_user = str(u.author)
            c.execute("INSERT OR IGNORE INTO upvotes_db VALUES (?,?,?,?,?,?)", (u.id, str_subreddit, u.title, u.link_flair_text, str_user, u.score))
            conn.commit()
        conn.close()
        

#random subreddit is chosen from the text file
    def fetch_posts(self):
        f = open("reddit titles.txt", "r")
        #populating a list based on the text lines
        lines = f.read().splitlines()
        f.close()
        length = len(lines)
        
        rand_temp = random.randint(0,length-1)
        
        sub = lines[rand_temp]
        
        subreddit_rand = self.reddit.subreddit(sub)
        
        fetch_results = subreddit_rand.hot(limit = 30)
        return fetch_results


#bot_one = bot_reach()
#bot_one.populate_upvotes('LachoBot')