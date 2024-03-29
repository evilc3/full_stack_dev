Blog Website

1. Read Operations
    a. Users will read the blogs.
    b. Users will read other comments.

2. Write operations
    a. Write a blog
    b. write comment or reply to a comment : (write chat.)

3. Read/Write Stat
    a. Its a read heavy system. System needs to be optimized for reads.
    b. write an have eventual consistency.


With eventual consistency for write.
a. for comments eventual consistency is ok there is no problem if user reads comments with a delay.
b. for write blogs.
    Its better for people to to be able to read the current version of the blog and notify about an update.
    Then to block the read for a particular until is written completely.


Hence with the above constraints the system is optimized for AP -> High Availability and Partation.

DataBase: For AP, high availability and Horizontal scaling going for No-Sql Database makes more sense.


How to run : docker run --name some-mongo -v /my/own/datadir:/data/db -d mongo
             docker run -p 27017:27017 -v ${pwd}:/data/db -d mongo

Functional Requirements

1. Authentication
2. Authorization
    a. A blog writer (a blog reader can also read blogs) so better reader-writer
    b. A blog reader
    c. A admin (can do all operations permitted by applications)
3. Read a blog.
4. Writing a blog.
5. Chat.
6. Search

(optional)
6. Link, DisLike, UpVote, DownVote
7. Personal Recommendations
8. Payed subscriptions.


'''
1. Able to move across the html pages and access the proper flask routes : done
2. Accept input from the html pages : done
3. Send data back to the html pages. : done
4. Check if all webpages are redirecting properly : done
5. Blogs can be created, previewed, deleted and viewed : done
6. Chat messages are supported and persistent. : done
7. app settings is taken care of : done

html pages here can be viewed as frontend
flask routes can be viewed as backend.

DataBase schema

1. UserInfo/BloggerDB DataBase (collection)
    This will store user information used for login/signup.
    Data Stored
       1. email
       2. Username (unspecified length)
       3. password hash
       4. password salt
       5. verified key a boolean to indicate the user is verified.

2. Blogs (collections)
    This will store the blogs the user rights.
       1. Blog Id for each blog (this will be based on user profile information).
       2. Blog Content (text)
       3. user_id
       4. Blog Name/Title

<!-- 3. UserLibrary (collections) -->
    <!-- This will store user library (all the user blogs) -->
       <!-- 1. user_id (user_id will be the email address.) -->
       <!-- 2. blog_id -->

4. ChatLibrary (collection)
    This will store user comments and chats for a particular blog.
       1. blog_id
       2. message
       3. type (type can be author/user)
'''

Blog Design
'''

Blog Page

Author Name: <username>
Author Email: <email>

Blog Content (for now only text.)

Chat Button
'''


