from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to establish a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to display the admin panel
@app.route('/')
def admin_panel():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM user').fetchall()
    comments = conn.execute('SELECT * FROM comments').fetchall()
    tweets = conn.execute('SELECT * FROM tweets').fetchall()
    retweets = conn.execute('SELECT * FROM retweet').fetchall()
    likes = conn.execute('SELECT * FROM likes').fetchall()
    conn.close()
    return render_template('admin_panel.html', users=users, comments=comments, tweets=tweets, retweets=retweets,likes=likes)

# Route to delete a user and associated comments and tweets
@app.route('/delete_user/<string:usrid>', methods=['POST'])
def delete_user(usrid):
    conn = get_db_connection()
    conn.execute('DELETE FROM user WHERE usrid = ?', (usrid,))
    conn.execute('DELETE FROM comments WHERE usrid = ?', (usrid,))
    conn.execute('DELETE FROM tweets WHERE usrid = ?', (usrid,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

# Route to delete a comment
@app.route('/delete_comment/<int:messageid>', methods=['POST'])
def delete_comment(messageid):
    conn = get_db_connection()
    conn.execute('DELETE FROM comments WHERE messageid = ?', (messageid,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/delete_tweet/<int:messageid>', methods=['POST'])
def delete_tweet(messageid):
    conn = get_db_connection()
    conn.execute('DELETE FROM tweets WHERE messageid = ?', (messageid,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

# Route to edit a tweet
@app.route('/edit_tweet/<int:messageid>', methods=['GET', 'POST'])
def edit_tweet(messageid):
    if request.method == 'POST':
        edited_msg = request.form['edited_msg']
        conn = get_db_connection()
        conn.execute('UPDATE tweets SET msg = ? WHERE messageId = ?', (edited_msg, messageid))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    else:
        conn = get_db_connection()
        tweet = conn.execute('SELECT * FROM tweets WHERE messageId = ?', (messageid,)).fetchone()
        conn.close()
        return render_template('edit_tweet.html', tweet=tweet)
    
@app.route('/edit_url/<string:usrid>', methods=['GET', 'POST'])
def edit_url(usrid):
    if request.method == 'POST':
        edited_url = request.form['edited_url']
        conn = get_db_connection()
        conn.execute('UPDATE user SET url = ? WHERE usrid = ?', (edited_url, usrid))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    else:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM user WHERE usrid = ?', (usrid,)).fetchone()
        conn.close()
        return render_template('edit_url.html', user=user)
    
@app.route('/edit_comment/<int:messageid>', methods=['GET', 'POST'])
def edit_comment(messageid):
    if request.method == 'POST':
        edited_comment = request.form['edited_comment']
        conn = get_db_connection()
        conn.execute('UPDATE comments SET comments = ? WHERE messageid = ?', (edited_comment, messageid))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    else:
        conn = get_db_connection()
        comment = conn.execute('SELECT * FROM comments WHERE messageid = ?', (messageid,)).fetchone()
        conn.close()
        return render_template('edit_comment.html', comment=comment)
    


@app.route('/delete_like/<int:messageid>/<string:usrid>', methods=['POST'])
def delete_like(usrid):
    conn = get_db_connection()
    conn.execute('DELETE FROM likes WHERE usrid = ?', (usrid))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))





@app.route('/edit_like/<int:messageid>/<string:usrid>', methods=['GET', 'POST'])
def edit_like(messageid, usrid):
    if request.method == 'POST':
        edited_usrid = request.form['edited_usrid']
        conn = get_db_connection()
        conn.execute('UPDATE likes SET usrid = ? WHERE messageid = ? AND usrid = ?', (edited_usrid, messageid, usrid))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    else:
        conn = get_db_connection()
        like = conn.execute('SELECT * FROM likes WHERE messageid = ? AND usrid = ?', (messageid, usrid)).fetchone()
        conn.close()
        return render_template('edit_like.html', like=like)



    
    




if __name__ == '__main__':
    app.run(debug=True,port=8080)
