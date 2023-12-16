API Documentation for Flask XTTS Service

## Overview
This api allows users to convert text into spoken audio. The service is built using Flask and wrapped around the TTS api. It uses the multi lang model **tts_models/multilingual/multi-dataset/xtts_v2**

### Base URL
```
http://localhost:5002
```

## Endpoints

### 1. Convert Text to Speech
Converts input text into spoken audio.

#### Endpoint
```
POST /convert
```

#### Request
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Body:**
  ```json
  {
    "text": "Hello, this is a sample text.",
    "speaker": "john",       // Speaker ID
    "speed": 1.0,            // Speech speed factor (1.0 is normal speed)
    "language": "en"         // Language code (e.g., "en" for English)
  }
  ```

#### Response
- **Content-Type:** `audio/wav`
- **Body:** Audio file containing the spoken text.

#### Example
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text": "Hello, this is a sample text.", "speaker": "john", "speed": 1.0, "language": "en"}' http://localhost:5002/convert > output.wav
```

### 2. Get List of Speakers
Retrieves the list of available speakers.

#### Endpoint
```
GET /speakers
```

#### Request
- **Method:** `GET`

#### Response
- **Content-Type:** `application/json`
- **Body:**
  ```json
  ["john", "jane", "smith"]
  ```

#### Example
```bash
curl http://localhost:5002/speakers
```

## Notes
- The API supports multiple languages, and language codes can be found in the `languages.json` file.
- The `speed` parameter allows adjusting the speech speed; 1.0 represents normal speed.
- The `/convert` endpoint applies noise reduction to the generated audio for improved quality.
- Speakers can be updated by adding new WAV files to the `targets` directory.

## Error Handling
- The API returns appropriate HTTP status codes for successful requests and errors.
- Detailed error messages are included in the response body for failed requests.

## Running the Service
To start the Flask app, run the following command in the terminal:
```bash
python app.py
```


Make sure to install the required dependencies using:
```bash
pip install Flask torch noisereduce librosa soundfile
```

or simply go to the main directory and 
```bash
pip install -r requirements.txt
```


## Future Improvements
I am thinking to wrap multiple more models like tacotron and others, and make it more easier to integrate into websites

Credits goes to the main model XTTS by Coqai you can check here [Coqui TTS GitHub Repository](https://github.com/coqui-ai/TTS)