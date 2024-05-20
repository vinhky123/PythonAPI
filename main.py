from flask import Flask, jsonify, request
from flask_cors import CORS
from process import crawl as cr
from process import preprocessing as pp
from model import modeling as md

import os
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def process_request(url):
    data = cr.crawl_shopee_comments(url)
    data_processed = pp.preprocess(data)
    return data_processed

@app.route('/', methods=['POST'])
def process():
    try:
        JScall = request.get_json()
        url = JScall['url']
        data = process_request(url)
        if data.empty == False:
            result_pos, result_neg, top_comment_positive, top_comment_negative, top_words_positive, top_words_negative = md.modeling(data)
        else:
            result_neg, result_pos, top_comment_positive, top_comment_negative, top_words_positive, top_words_negative = 0, 0, [], [], [], []
        print(result_pos, result_neg, top_comment_positive, top_comment_negative, top_words_positive, top_words_negative)
        return jsonify({"positive": result_pos, 
                        "negative": result_neg, 
                        "top_positive_comments": top_comment_positive, 
                        "top_negative_comments" : top_comment_negative,
                        "top_positive_words": top_words_positive,
                        "top_negative_words": top_words_negative 
                        }), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)