
import re
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Hàm trích xuất tên và số điện thoại từ nội dung tin nhắn
def extract_info(text):
    phone_pattern = r"(0|\+84)\d{9,10}"
    phone_number = re.search(phone_pattern, text)
    phone_number = phone_number.group() if phone_number else None

    name_pattern = r"Tên tôi là (\w+)"
    name = re.search(name_pattern, text)
    name = name.group(1) if name else None

    return name, phone_number

# Định nghĩa endpoint webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message_text = data['entry'][0]['messaging'][0]['message']['text']
    name, phone_number = extract_info(message_text)

    df = pd.DataFrame([{'Name': name, 'Phone Number': phone_number}])
    df.to_excel('extracted_info.xlsx', index=False)

    return jsonify({'status': 'success', 'name': name, 'phone_number': phone_number})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
