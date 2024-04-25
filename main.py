from flask import Flask, jsonify, request
from flask_cors import CORS
from process import crawl as cr
from process import preprocessing as pp
import pickle
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def process_request(url):
    data = cr.crawl_shopee_comments(url)
    data_processed = pp.preprocess(data)
    return data_processed

def modeling(data):
    with open('./model/model_lr.pkl', 'rb') as f:
        model_ = pickle.load(f)
    result = model_.predict(data['comment'])
    positive = 0
    negative = 0
    for i in range(len(result)):
        if result[i] == 1:
            positive += 1
        elif result[i] == 0:
            negative += 1
    return positive, negative

@app.route('/api', methods=['POST'])
def process():
    # Nhận dữ liệu từ yêu cầu POST
    url = request.json
    data = process_request(url)
    result_pos, result_neg = modeling(data)
    return jsonify(result_pos, result_neg)

if __name__ == '__main__':
    app.run(debug=True)