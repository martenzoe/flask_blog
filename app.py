from flask import Flask, render_template, json, request, redirect, url_for
import json

app = Flask(__name__)

# Blog-Beiträge aus der JSON-Datei lesen
with open('blog_posts.json', 'r') as file:
    blog_posts = json.load(file)

@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    global blog_posts
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        # Generieren einer eindeutigen ID
        new_id = max([post['id'] for post in blog_posts], default=0) + 1

        # Neuen Blog-Beitrag erstellen
        new_post = {
            'id': new_id,
            'title': title,
            'content': content
        }

        # Beitrag zur Liste hinzufügen
        blog_posts.append(new_post)

        # Speichern der aktualisierten blog_posts in der JSON-Datei
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    global blog_posts
    # Finden und Entfernen des Blog-Posts mit der gegebenen ID
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Aktualisieren der JSON-Datei
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

    # Zurück zur Startseite
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    global blog_posts
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Update the JSON file
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    # If it's a GET request, display the update form
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
