from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load blog posts from the JSON file
try:
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)
except FileNotFoundError:
    blog_posts = []
except json.JSONDecodeError:
    blog_posts = []


@app.route('/')
def index():
    """
    Render the home page with a list of all blog posts.
    """
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle adding a new blog post.
    - On GET: Render the form to add a new post.
    - On POST: Add the new post to the list and save it to the JSON file.
    """
    global blog_posts

    if request.method == 'POST':
        try:
            title = request.form.get('title')
            content = request.form.get('content')

            # Generate a unique ID for the new post
            new_id = max([post['id'] for post in blog_posts], default=0) + 1

            # Create the new blog post
            new_post = {
                'id': new_id,
                'title': title,
                'content': content
            }

            # Add the new post to the list
            blog_posts.append(new_post)

            # Save the updated list to the JSON file
            with open('blog_posts.json', 'w') as file:
                json.dump(blog_posts, file, indent=4)

            return redirect(url_for('index'))

        except Exception as e:
            return f"An error occurred while adding the post: {e}", 500

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Handle deleting a blog post by its ID.
    - Remove the post from the list and update the JSON file.
    """
    global blog_posts

    try:
        # Find and remove the post with the given ID
        blog_posts = [post for post in blog_posts if post['id'] != post_id]

        # Update the JSON file
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    except Exception as e:
        return f"An error occurred while deleting the post: {e}", 500


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handle updating an existing blog post.
    - On GET: Render a form pre-filled with the current details of the post.
    - On POST: Update the details of the post and save it to the JSON file.
    """
    global blog_posts

    try:
        # Find the post by its ID
        post = next((post for post in blog_posts if post['id'] == post_id), None)
        if not post:
            return "Post not found", 404

        if request.method == 'POST':
            # Update the post details
            post['title'] = request.form.get('title')
            post['content'] = request.form.get('content')

            # Save the updated list to the JSON file
            with open('blog_posts.json', 'w') as file:
                json.dump(blog_posts, file, indent=4)

            return redirect(url_for('index'))

        # Render the update form for a GET request
        return render_template('update.html', post=post)

    except Exception as e:
        return f"An error occurred while updating the post: {e}", 500

@app.route('/like/<int:post_id>')
def like(post_id):
    """
    Increment the 'likes' count for a specific blog post.
    """
    global blog_posts

    try:
        # Find the post by its ID
        post = next((post for post in blog_posts if post['id'] == post_id), None)
        if not post:
            return "Post not found", 404

        # Increment the 'likes' count (initialize to 0 if not present)
        post['likes'] = post.get('likes', 0) + 1

        # Save the updated list to the JSON file
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        # Redirect back to the index page
        return redirect(url_for('index'))

    except Exception as e:
        return f"An error occurred while liking the post: {e}", 500


if __name__ == '__main__':
    """
    Run the Flask application on host 0.0.0.0 and port 5001 in debug mode.
    """
    app.run(host="0.0.0.0", port=5000, debug=True)
