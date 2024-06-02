from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from process import crawl as cr
from process import preprocessing as pp
from model import modeling as md
from matplotlib import pyplot as plt
import time
import io

import os
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def process_request(url):
    data, number = cr.crawl_shopee_comments(url)
    data_processed = pp.preprocess(data)
    return data_processed, number

@app.route('/analyse', methods=['POST'])
def process():
    try:
        JScall = request.get_json()
        url = JScall['url']
        if "https://shopee.vn/" not in url:
            return jsonify({"error": "URL is not from Shopee"}), 200
        data, number = process_request(url)
        if data.empty == False:
            result_pos, result_neg, top_comment_positive, top_comment_negative, top_words_positive, top_words_negative = md.modeling(data)
        else:
            result_neg, result_pos, top_comment_positive, top_comment_negative, top_words_positive, top_words_negative = 0, 0, [], [], [], []

        return jsonify({"number_comment": number,
                        "positive": result_pos, 
                        "negative": result_neg, 
                        "top_positive_comments": top_comment_positive, 
                        "top_negative_comments" : top_comment_negative,
                        "top_positive_words": top_words_positive,
                        "top_negative_words": top_words_negative 
                        }), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
'''
@app.route('/drawPLot', methods=['POST'])
def draw_plot():
    # Get the data from the request (you'll need to parse the JSON)
    # For simplicity, I'm using fixed data
    data = {'red': 10, 'green': 20, 'grey': 70}
    labels = list(data.keys())
    sizes = list(data.values())

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)

    return send_file(bytes_image, mimetype='image/png')

'''

if __name__ == '__main__':
    app.run(debug=True)