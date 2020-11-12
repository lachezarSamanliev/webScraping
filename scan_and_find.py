import praw
import sqlite3
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from db_upvotes import db_helper
from reddit_bot import bot_reach



class Scanner:
    def __init__(self):
        
        self.count = Counter()
        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.db_reach = db_helper()
        
        
    def update_keywords(self):

        result = self.db_reach.fetch("SELECT title FROM upvotes_db")

        word_tokens = word_tokenize(str(result))
        filtered_sentece = [w for w in word_tokens if not w in self.stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in self.stop_words:
                filtered_sentence.append(self.wordnet_lemmatizer.lemmatize(w))

        counted_words = Counter(filtered_sentence)
        
        conn = sqlite3.connect('keywords_instances')
        c = conn.cursor()
        
        #populate keywords database
        duration = len(counted_words)
        for x in range (0, duration):
            #if instance of keyword is more than twice
            if counted_words.most_common()[x][1] >= 2:
                #populate
                temp_word = counted_words.most_common()[x][0]
                temp_num = counted_words.most_common()[x][1]
                
                c.execute("INSERT OR IGNORE INTO keywords_instances VALUES (?,?)", (temp_word, temp_num))
                conn.commit()
                print("inserted")
            else:
                print("requirements did not fit")
                print("")
        conn.close()


#fetch keywords from DB
#fetch observed titles and split in words
#comapre words with for statements

#fetch user from db
#fetch subreddits from db

    def estimate_recommend(self):
        #fetch keywords
        conn = sqlite3.connect('keywords_instances')
        c = conn.cursor()

        c.execute("SELECT keyword FROM keywords_instances")
        list_keywords = (c.fetchall())
        conn.close()
        
        l_keywords = []
        #transfer keywords to list
        len_k = len(list_keywords)
        for x in range(0,len_k):
            l_keywords.append(list_keywords[x][0])
            
        #fetch users and subreddits from db.
        result_authors = self.db_reach.fetch("SELECT user FROM upvotes_db")
        l_authors = []
        len_a = len(result_authors)
 
        for x_two in range(0,len_a):
            l_authors.append(result_authors[x_two][0])

        result_subreddits = self.db_reach.fetch("SELECT subreddit FROM upvotes_db")
        #print(result_subreddits[2][0])
        l_subreddits = []
        len_s = len(result_subreddits)
        for x_three in range(0,len_s):
            l_subreddits.append(result_subreddits[x_three][0])

        #removing duplicates so they don't get checked twice or more times
        l_subreddits = list(dict.fromkeys(l_subreddits))
        
        #fetching info of the random posts
        titles = []
        authors = []
        subreddits = []
        ids = []
        
        #code to fetch 30 posts from random subreddit
        reddit_access = bot_reach()
        full_list = reddit_access.fetch_posts()

        for u in full_list:
            #print(u.title)
            titles.append(u.title)
            authors.append(u.author)
            subreddits.append(u.subreddit)
            ids.append(u.id)

        len_keywords = len(l_keywords)
        #showing subreddit checked
        temp_sub = subreddits[0]
        print("For the subreddit " + str(temp_sub))
        print("")
        
        for x_post in range (1,30):
            #keep track of score so that you can recommend
            score_for_recommend = 1
            temp_title = titles[x_post].split()
            #using set and bool result to know if there are matches compared to keywords
            result_k = set(l_keywords).intersection(temp_title)
            #print(len(what))
            
            if len(result_k) == 1:
                #print("IT IS 1")
                score_for_recommend += 1
            elif len(result_k) == 2:
                score_for_recommend += 2
            
            #comapre for author
            result_a = bool(set(l_authors).intersection(authors))
            if result_a == True:
                score_for_recommend += 1
            #print(result_s)
            #compare for subreddit
            result_s = bool(set(l_subreddits).intersection(subreddits))
            #print(result_s)
            if result_s == True:
                score_for_recommend += 1

            if score_for_recommend >= 2:
                temp_sub = subreddits[x_post]
                #print("Recommended post  in subreddit " + str(temp_sub) +" with link")
                print("Recommended post with link")
                
                temp_id = ids[x_post].split()
                url = "https://reddit.com/" + temp_id[0]
                print(url)
                print("")



#n = Scanner()
#scan.estimate_recommend()
#scan.update_keywords()