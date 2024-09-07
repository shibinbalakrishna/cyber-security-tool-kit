import sqlite3

# Function to fetch tweets from the database
def get_tweets():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT usrid, msg FROM tweets")
    tweets = cursor.fetchall()
    conn.close()
    return tweets

# Function to fetch limited blog posts from the database
def get_blog_posts(limit=4):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT usrid, msg FROM tweets LIMIT ?", (limit,))
    blog_posts = cursor.fetchall()
    conn.close()
    return blog_posts



