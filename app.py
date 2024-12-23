from flask import Flask, request, jsonify, render_template, redirect
import instaloader
import re

app = Flask(__name__)
loader = instaloader.Instaloader()


def get_reel_description(reel_url):
    match = re.search(r'/reel/([^/?]+)', reel_url)
    if not match:
        return "Invalid Reel URL"

    shortcode = match.group(1)
    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        return post.caption or "No description available."
    except Exception as e:
        return f"Error: {e}"


# Home route - Display form
@app.route('/')
def index():
    return render_template('index.html', description='')


@app.route('/get_description_from_form', methods=['POST'])
def get_description_form():
    reel_url = request.form.get('url')
    if not reel_url:
        return jsonify({"error": "No URL provided"}), 400

    description = get_reel_description(reel_url)
    print(description)
    return render_template('index.html', description=description)

@app.route('/get_description_from_share', methods=['POST'])
def get_description_share():
    if request.is_json:
        data = request.json
        reel_url = data.get("url")
    if not reel_url:
        return jsonify({"error": "No URL provided"}), 400

    description = get_reel_description(reel_url)
    print('from share')
    return jsonify({'description': description})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
