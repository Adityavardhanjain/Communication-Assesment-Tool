---
name: "Communication Assessment Tool"
about: Comprehensive communication assessment tool with video proctoring
labels: NLP Communication Assessment 

---

# Assessment Tools within the Software

(https://github.com/Adityavardhanjain/Communication-Assesment-Tool/assets/110587290/8da8aec3-8603-464d-9c3e-66e5eec1c357)


## Writing Assessment Tool

To check for grammar, Python language tool uses Statistical language modelling (prediction on basis of where the next word shoukd be) and Rule based approach (multiple grammmar rules) which takes text input, gives out the error, explains which rule is violated and gives appropriate suggestions by using a rule ID. 

## Listening Assessment Tool

The tool gives a randomly generated speech prompt, asks the user to repeat it and records & compares the 2 to asess user's listening skills. It also uses homogenous temporal segments to check for pronunciation.

## Speaking Assesment Tool

The tool gives out a randomly generated text, takes in an input in the form of speech and uses the previously mentioned pronunciation model along with a fluency model that uses spectral analysis of the audio files. It also uses a model to count for intonation to account for voice modulation.

## Presentation Assessment Tool

The tool takes in an input video, gives it a understandibility score on the basis of Gunning_Fog and Flesch_Kincaid Readability Tests. It also checks it for grammar, pronunciation, intonation, filler sounds and fluency by previously mentioned models.

# Video Proctoring

The video is being recorded by OpenCV library of Computer Vision. The point estimation is done by FaceMesh which uses confidence score for detetction and tracking. Coordinates are assigned on the basis of the point. Based on the position of these points, we can precisely predict where a person is looking. 

For the cases where no point is detected, a message of "Please stay in the range of the web camera" is displayed. 

For the cases where a person is not looking at the screen (coordinate geometry and linear algebra on the face point tensors), a message of "Please look at the web camera appears"

The web cam runs in the background without disturbance for all other cases.

# Steps to reproduce

1. Download all requirements (See requirements.txt)
2. Allow microphone, web camera and file access from your browser
3. Run main.py
4. Use your own examples or the ones given in demo files


### Additional context
The project uses CNN, RNN, NLP, TensorFlow and several other high processing power requiring tool some of which work in real time as well (Video Proctoring and Grammar Checker). It is recommended using a system with processing power akin to Intel core i5 or higher. 
