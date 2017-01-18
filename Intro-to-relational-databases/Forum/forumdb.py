#
# Database access functions for the web forum.
#

import psycopg2
import bleach


# Database connection


# Get posts from database.


def GetAllPosts():
    """Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    """
    conn = psycopg2.connect(database="forum", user="mohamedelzarei")
    db = conn.cursor()
    db.execute('SELECT * FROM posts ORDER BY time')
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in
             db.fetchall()]
    conn.close()
    return posts


# Add a post to the database.


def AddPost(content):
    """Add a new post to the database.

    Args:
      content: The text content of the new post.
    """
    conn = psycopg2.connect(database="forum", user="mohamedelzarei")
    db = conn.cursor()
    db.execute("INSERT INTO posts(content) VALUES (%s);", (bleach.clean(content),))
    conn.commit()
    conn.close()
