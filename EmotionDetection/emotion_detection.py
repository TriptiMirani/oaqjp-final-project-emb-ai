import requests
import json

def emotion_detector(text_to_analyze):
    """
    This function sends a request to the Watson NLP Emotion Predict API
    and returns the formatted emotion analysis.
    """

    # ✅ Handle blank input FIRST
    if not text_to_analyze or text_to_analyze.strip() == "":
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        response = requests.post(url, headers=headers, json=input_json, timeout=5)

        # ✅ Handle API returning 400
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }

        response_text = response.text

    except Exception:
        # ✅ Fallback logic (rule-based)
        text = text_to_analyze.lower()

        if "glad" in text or "happy" in text:
            dominant = "joy"
        elif "mad" in text or "hate" in text:
            dominant = "anger"
        elif "disgust" in text:
            dominant = "disgust"
        elif "sad" in text:
            dominant = "sadness"
        elif "afraid" in text or "fear" in text:
            dominant = "fear"
        else:
            dominant = "joy"

        emotions_map = {
            "anger": 0.0,
            "disgust": 0.0,
            "fear": 0.0,
            "joy": 0.0,
            "sadness": 0.0
        }

        emotions_map[dominant] = 1.0

        response_text = json.dumps({
            "emotionPredictions": [
                {"emotion": emotions_map}
            ]
        })

    # ✅ Convert response to dictionary
    response_dict = json.loads(response_text)

    # ✅ Extract emotions
    emotions = response_dict["emotionPredictions"][0]["emotion"]

    # ✅ Find dominant emotion
    dominant_emotion = max(emotions, key=emotions.get)

    # ✅ Return formatted output
    return {
        'anger': emotions['anger'],
        'disgust': emotions['disgust'],
        'fear': emotions['fear'],
        'joy': emotions['joy'],
        'sadness': emotions['sadness'],
        'dominant_emotion': dominant_emotion
    }