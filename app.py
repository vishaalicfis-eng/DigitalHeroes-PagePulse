from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():

    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({"error": "Please provide a URL"}), 400

    url = data['url']

    # Validate URL
    if not url.startswith(("http://", "https://")):
        return jsonify({
            "success": False,
            "message": "Please enter a valid URL starting with http:// or https://"
        }), 400
    
    print("=" * 50)
    print("Analyzing Website")
    print("URL:", url)
    print("=" * 50)

    try:
        start = time.time()

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        end = time.time()

        response_time = round((end - start) * 1000, 2)

        content_type = response.headers.get("Content-Type", "")

        if "text/html" not in content_type:
            return jsonify({
                "error": "The provided URL is not an HTML webpage."
            })

        soup = BeautifulSoup(response.text, "html.parser")

        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else "No Title"
    )

        meta = soup.find("meta", attrs={"name": "description"})
        meta_description = meta["content"] if meta and meta.get("content") else "Not Available"

        h1_count = len(soup.find_all("h1"))

        images = soup.find_all("img")
        links = soup.find_all("a")
        h2_count = len(soup.find_all("h2"))
        canonical = soup.find("link", rel="canonical")
        canonical_present = "Yes" if canonical else "No"
        missing_alt = len([img for img in images if not img.get("alt")])

        text = soup.get_text(separator=" ")
        word_count = len(text.split())
        # Calculate SEO Score
        seo_score = 100

        if missing_alt > 0:
            seo_score -= 10
        if h1_count == 0:
            seo_score -= 15
        if meta_description == "Not Available":
            seo_score -= 15
        if canonical_present == "No":
            seo_score -= 10
        if h2_count == 0:
            seo_score -= 10

        return jsonify({
            "HTTP Status": response.status_code,
            "Response Time (ms)": response_time,
            "Title": title,
            "Meta Description": meta_description,
            "H1 Count": h1_count,
            "H2 Count": h2_count,
            "Total Images": len(images),
            "Images Missing Alt": missing_alt,
            "Total Links": len(links),
            "Canonical Tag": canonical_present,
            "Approximate Word Count": word_count,
            "SEO Score": seo_score
        })

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "The website took too long to respond."
        }), 408

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Unable to connect to the website."
        }), 503

    except requests.exceptions.HTTPError:
        return jsonify({
            "error": "The website returned an HTTP error."
        }), 500

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
