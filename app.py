import secrets
from flask import Flask, render_template, request, redirect, url_for
from forms import WritingForm, ShitpostingForm, PasswordForm
import writing_db
import shitposts_db

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(64)


def verify_key(password):
    with open("password.key", "r") as key_file:
        stored_password = key_file.read().strip()
        return password == stored_password


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/writings")
def writings():
    return render_template("writings.html", writing_posts=writing_db.get_all())


@app.route("/shitposts")
def shitposts():
    return render_template("shitposts.html", shitpost_posts=shitposts_db.get_all())


@app.route("/create-writing", methods=["GET", "POST"])
def create_writings():
    writing_form = WritingForm()
    if request.method == "POST":
        if writing_form.validate_on_submit():
            title = writing_form.title.data
            subtitle = writing_form.subtitle.data
            content = writing_form.content.data
            password = writing_form.password.data
            if verify_key(password):
                writing_db.create_writing(title, subtitle, content)
                return redirect(url_for("writings"))
    return render_template("create_writing.html", writing_form=writing_form)


@app.route("/create-shitposts", methods=["GET", "POST"])
def create_shitposts():
    shitposting_form = ShitpostingForm()
    if request.method == "POST":
        if shitposting_form.validate_on_submit():
            username = shitposting_form.username.data
            content = shitposting_form.content.data
            shitposts_db.create_shitpost(username, content)  # Corrected function name
            return redirect(url_for("shitposts"))
    return render_template("create_shitposts.html", shitposting_form=shitposting_form)


@app.route("/read/<int:post_id>")
def read(post_id: int):
    return render_template("read.html", post=writing_db.get_writing(post_id))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/manage", methods=["GET", "POST"])
def manage():
    password_form = PasswordForm()
    if request.method == "POST":
        if password_form.validate_on_submit():
            password = password_form.password.data
            if verify_key(password):
                writing_posts = writing_db.get_all()
                shitpost_posts = shitposts_db.get_all()
                return render_template(
                    "manage.html",
                    writing_posts=writing_posts,
                    shitpost_posts=shitpost_posts,
                    password_verified=True,
                )
            else:
                return redirect(url_for("index"))
    return render_template("manage.html", password_form=password_form)


@app.route("/delete-writing/<int:post_id>", methods=["POST"])
def delete_writing(post_id):
    writing_db.delete_writing(post_id)
    return redirect(url_for("manage"))


@app.route("/delete-shitpost/<int:post_id>", methods=["POST"])
def delete_shitpost(post_id):
    shitposts_db.delete_shitpost(post_id)
    return redirect(url_for("manage"))


if __name__ == "__main__":
    writing_db.create_table()
    shitposts_db.create_table()
    app.run(debug=False)
