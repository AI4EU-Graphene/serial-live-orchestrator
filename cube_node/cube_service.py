from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/cube', methods=['POST'])
def cube_number():
    try:
        data = request.get_json()
        number = data.get('number', None)

        if number is None:
            return jsonify({'error': 'Missing number in request'}), 400

        result = number ** 3
        return jsonify({'input': number, 'output': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/', methods=['GET'])
def root():
    return "Cube node is running.", 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
