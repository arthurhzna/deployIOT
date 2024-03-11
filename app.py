from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

data_received = {"sensorValue": None, "relayStatus": None}
mode = 1
kondisi = 0

@app.route('/check_mode', methods=['GET'])  
def check_mode():  
    return jsonify({'mode': mode})

@app.route('/set_mode/<int:new_mode>', methods=['GET'])
def set_mode(new_mode):
    global mode
    mode = new_mode
    return jsonify({'message': f'Mode has been set to {mode}'}), 200

@app.route('/check_kondisi', methods=['GET'])
def check_kondisi():  
    status = 'ON' if kondisi == 1 else 'OFF'
    return jsonify({'kondisi': status})

@app.route('/set_kondisi/<int:new_kondisi>', methods=['GET'])
def set_kondisi(new_kondisi):
    global kondisi
    kondisi = new_kondisi
    return jsonify({'message': f'Mode has been set to {new_kondisi}'}), 200

@app.route('/receive_data', methods=['POST'])
def receive_data():
    global data_received
    if request.method == 'POST':
        data = request.json
        if data:
            timestamp_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data_received["sensorValue"] = data.get('sensorValue')
            data_received["relayStatus"] = data.get('relayStatus')
            response = {"message": "Data received successfully"}

            with open('data.txt', 'a') as file:
                file.write(f"{data_received['sensorValue']} {data_received['relayStatus']} {timestamp_str}\n")
            return jsonify(response), 200
        else:
            return jsonify({"error": "No JSON data received"}), 400
    else:
        return jsonify({"error": "Only POST requests are allowed"}), 405

@app.route('/check_data', methods=['GET'])
def check_data():
    global data_received
    return jsonify(data_received), 200

if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)))