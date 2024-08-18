from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['GET', 'POST'])
def emotion_detector_route():
    if request.method == 'POST':
        data = request.json
        text = data.get('text')
    elif request.method == 'GET':
        text = request.args.get('textToAnalyze')

    if not text:
        return jsonify({"response": "Invalid text! Please try again."}), 400

    result = emotion_detector(text)
    if result['dominant_emotion'] is None:
        return jsonify({"response": "Invalid text! Please try again."}), 400

    response = {
        "anger": result['anger'],
        "disgust": result['disgust'],
        "fear": result['fear'],
        "joy": result['joy'],
        "sadness": result['sadness'],
        "dominant_emotion": result['dominant_emotion']
    }

    formatted_response = (
        f"For the given statement, the system response is 'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, 'fear': {response['fear']}, 'joy': {response['joy']} "
        f"and 'sadness': {response['sadness']}. The dominant emotion is {response['dominant_emotion']}."
    )

    return jsonify({"response": formatted_response})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
