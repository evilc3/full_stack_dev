from flask import Flask, render_template, request, make_response, redirect, session, url_for, flash
from utils import find_blogs, generate_verification_code, hash_password, verify_password, send_email, generate_blog_id
from flask_mail import Mail
# from flaskext.markdown import Markdown
import markdown
from db import mongodb, mongodb_blog, mongodb_chat
from time import perf_counter, sleep
# from blog_website import create_app

app = Flask(__name__)

app.secret_key = "clive69"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'clivefernandes20@gmail.com'  # Your Gmail email address
app.config['MAIL_PASSWORD'] = 'weww gpah mqdb jfax'  # Your Gmail password or app-specific password
app.config['MAIL_DEFAULT_SENDER'] = 'clivefernandes20@gmail.com'  # Your Gmail email address

# Markdown(app)
mail = Mail(app)

@app.route('/', methods=['GET'])
def index():

    print('Session : ', session)

    if 'username' in session:
        ###print a banner message.
        flash(f"Login Successful for user {session.get('username')}", "success")
        return redirect(url_for('gallery'))

    return render_template('index.html')

@app.route('/blogger/settings/', methods=['GET', 'POST'])
def settings():

    user_details = mongodb.get(query={'email': session['username']})

    if request.method == 'POST':
        ###check if we want to change the password.
        password = request.form.get("password")
        change_password = request.form.get("change_password")
        current_passwords = request.form.get("current_password")

        ###verify the current password is correct.
        correct_password = verify_password(password=current_passwords,
                                           hashed_password=user_details['password_hash'],
                                           salt=user_details['password_salt'])

        if not correct_password:
            return "Incorrect password."

        ###create new salts
        password_hash, password_salt = hash_password(password=password)

        ###update the mongo db
        update_query = {'$set': {'password_hash': password_hash, 'password_salt': password_salt}}
        mongodb.update(email_id=user_details['email'], update_query=update_query)

    ###using the session get the user details from the db
    # user_details = mongodb.get(email_id=session['username'])

    return render_template('settings.html', **user_details)

@app.route('/blogger/user_library', methods=['GET', 'POST'])
def user_library():
    print('In user library')

    ###get all blogs by an specific user.
    blogs = mongodb_blog.get_all({'user_id': session['username']})

    # print('All blogs : ', blogs)

    return render_template('library.html', blogs = blogs)

@app.route('/blogger/gallery', methods=['GET', 'POST'])
def gallery():

    print('IN gallery')

    if request.method == 'POST':

        ###get the search term.
        search_query = request.form.get("search")

        print("search query : ", search_query)

        if search_query and search_query.strip() != "":

            blog_titles = mongodb_blog.get_top_searches(search_query)

            # print('Blogs : ', blog_titles)

            return render_template('gallery.html', blogs=blog_titles)

    return render_template('gallery.html', blogs=find_blogs())

@app.route('/blogger/create_blog', methods=['GET', 'POST'])
def create_blog():

    html_blog = ""

    if request.method == 'POST':
        # return render_template('create_blog.html')
        blog_name = request.form.get('title')
        html_blog = markdown.markdown(request.form['markdownInput'])
        # preview_html = marked(markdown_input)

        ###get information of current user.
        user_data = mongodb.get(query={'email': session['username']})

        ###generate unique id for blog
        code = generate_blog_id(content=user_data['email'] + ' ' + blog_name + ' ' + html_blog)

        ####insert this into the mongodb.
        document = {'blog_id': code,
                    'user_id': user_data['email'],
                    'blog': html_blog,
                    'title': blog_name,
                    }

        mongodb_blog.put(document)

        mongodb_blog.print_db()

    return render_template('create_blog.html', preview=html_blog)

@app.route('/blogger/signup', methods=['GET', 'POST'])
def signup():

    error = None
    t1 = perf_counter()
    print('In signup page ...')

    print('Request Data : >>>', request.data, request.form)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get("confirm_password")
        email = request.form.get("email")
        verification_code = generate_verification_code(email)
        pw_hash, pw_salt = hash_password(password)
        item = {'username':username, 'email': email, 'verification_code':verification_code, 'password_hash': pw_hash, 'password_salt': pw_salt}

        if username.strip() == '' or password.strip() == "" or email.strip() == "" or confirm_password.strip() == "":
            return render_template('signup.html', error=True)

        ###check if the email already exists dont add instead redirect to login page.

        if mongodb.get({'email': email}):
            flash(f"User {email} already registered login.", "info")
            return redirect(url_for('login'))

        send_email(mail, item)
        # sleep(3)

        flash("Check your email address for the verification mail!!!", "info")

        # local_db[email] = item

        mongodb.put(item)

        mongodb.print_db()

        print('Signup Time Taken :', perf_counter() - t1)

        return redirect(url_for('login'))

    return render_template('signup.html', error=error)

@app.route('/blogger/login', methods=['GET', 'POST'])
def login():
    print('In login page ...')
    mongodb.print_db()
    error = None

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        # user_data = local_db.get(username)
        user_data = mongodb.get(query={'email': username})

        if not user_data:
            # return "User not found."
            flash("User not found, please signup.", "info")
            return redirect(url_for("signup"))
        elif 'verified' not in user_data or not user_data['verified']:
            return "User not verified."

        pwd_hash = user_data['password_hash']
        pwd_salt = user_data['password_salt']

        if verify_password(password, pwd_hash, pwd_salt):
            error = None
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = "Unable to login"

    return render_template('login.html', error=error)

@app.route('/verify/<email>/<verification_code>')
def verify(email, verification_code):
    # user = local_db.get(email)

    mongodb.print_db()

    user = mongodb.get(query={'email': email})

    print('Verificaiton code : ', verification_code)
    print('database item : ', user)
    # print('User info :', user)
    # print(user['verification_code'] == verification_code)

    if user and str(user['verification_code']) == str(verification_code):
        # Mark user as verified in the database
        # del local_db[email]['verification_code']

        update_operations = {
                '$set': {'verified': True},  # Add a new key called 'verified' with value True
                '$unset': {'verification_code': ''}  # Remove the key 'verification_code'
            }

        mongodb.update({'email': user['email']}, update_operations)

        flash('Email verified successfully. You can now log in.', 'success')
    else:
        flash('Invalid verification code.', 'error')

        update_operations = {
                '$set': {'verified': False},  # Add a new key called 'verified' with value True
                '$unset': {'verification_code': ''}  # Remove the key 'verification_code'
            }

        mongodb.update(user['email'], update_operations)

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    ####clear the session
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/show_blog/<blog_id>/')
def show_blog(blog_id):

    print('In show blog, blog id : ', blog_id)

    ###get the blog data
    blog_info = mongodb_blog.get(query={'blog_id': blog_id})

    print('Blog Info : ', blog_info)

    if not blog_info: return "Blog not found"

    email = blog_info["user_id"]

    ### get user information
    user_info = mongodb.get(query={'email': email})

    blog_id = blog_info["blog_id"]
    blog_title = blog_info["title"]
    blog_content = blog_info["blog"]
    author_name = user_info['username']

    return render_template('blog.html',
                           author_name=author_name,
                           blog_title=blog_title,
                           blog_content=blog_content,
                           email=email,
                           blog_id=blog_id,
                           )

@app.route('/blogger/<blog_id>/chat/', methods=['POST', 'GET'])
def chat(blog_id):

    ###get blog details
    blog_details = mongodb_blog.get({'blog_id': blog_id})

    chat_messages = mongodb_chat.get_all(query={'blog_id': blog_id})

    if request.method == 'POST':
        ###need to add this to the chat message

        ###need to maintain the order of the chats, lets create an counter variable

        ###check if chats messages for this blogs already exists.
        if not chat_messages:
            order_number = 0
        else:
            chat_messages = list(chat_messages)
            order_number = len(chat_messages)

        document = {
                    'blog_id': blog_id,
                    'content': request.form['message'],
                    'type': 'author' if session['username'] == blog_details['user_id'] else 'user',
                    'order_number': order_number
                    }

        mongodb_chat.put(document)

        ###append the latest message
        chat_messages.append(document)

    all_chat_messages = sorted(chat_messages, key = lambda x : x['order_number'])

    return render_template('chat.html', messages=all_chat_messages)

@app.route('/blogger/delete_blog/<blog_id>', methods = ['POST', 'GET'])
def delete_blog(blog_id):

    ###get the blog data
    blog_info = mongodb_blog.get(query={'blog_id': blog_id})

    if not blog_info: return "Blog not found"

    if request.method  == 'POST':
        ### need to delete the post.
        message = request.form.get("text_area")

        if message.lower().strip() != 'delete': return "Failed to delete"

        delete_query = {'blog_id': blog_id}
        mongodb_blog.delete(delete_query)
        return redirect(url_for('index'))

    return render_template('delete_blog.html', blog_title=blog_info['title'])

if __name__ == '__main__':
    app.run('0.0.0.0', port = '8000', debug = True)