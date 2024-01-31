import secrets
from flask import Flask, render_template, request, redirect, url_for
from forms import WritingForm, ShitpostingForm
import writing_db
import shitposts_db

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(32)


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
            if password == "yourmom123":
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
            shitposts_db.create_writing(username, content)

            return redirect(url_for("shitposts"))

    return render_template("create_shitposts.html", shitposting_form=shitposting_form)


@app.route("/read/<int:post_id>")
def read(post_id: int):
    return render_template("read.html", post=writing_db.get_writing(post_id))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    writing_db.create_table()
    shitposts_db.create_table()
    app.run(debug=True)
