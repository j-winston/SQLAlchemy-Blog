from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = StringField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/show_post/<int:index>", methods=['GET', 'POST'])
def show_post(index):
    posts = db.session.query(BlogPost).all()

    requested_post = None
    for blog_post in posts:
        if blog_post.id == index:
            requested_post = blog_post

    return render_template("show_post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/edit-post/<post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    # Show blog post
    if request.method == 'GET':
        blog_post = BlogPost.query.get(post_id)
        edit_form = CreatePostForm()
        edit_form.title.data = blog_post.title
        edit_form.subtitle.data = blog_post.subtitle
        edit_form.author.data = blog_post.author
        edit_form.img_url.data = blog_post.img_url
        edit_form.body.data = blog_post.body
        return render_template("make-post.html", post=blog_post, edit_form=edit_form)
    # For updating blog post
    elif request.method == 'POST':
        blog_post = BlogPost.query.get(post_id)
        blog_post.author = request.form['author']
        blog_post.title = request.form['title']
        blog_post.subtitle = request.form['subtitle']
        blog_post.img_url = request.form['img_url']
        blog_post.body = request.form['body']
        db.session.commit()

        return redirect("/")


@app.route("/new-post", methods=['GET', 'POST'])
def new_post():
    new_form = CreatePostForm()
    return render_template("make-post.html", new_form=new_form)


@app.route("/delete/<post_id>")
def delete(post_id):
    post = BlogPost.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
