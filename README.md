# Air-Board

An application that allows user to draw on air, recognizing the text written on air and projecting the text on an AR environment.

# Basic Architecture

![image](https://user-images.githubusercontent.com/53861812/172015157-a080fcc7-e7e9-4cd1-9dcd-bd363e210914.png)

# Hand Tracking

Live tracking of hands is done using mediapipe, a cross platform library developed by Google that provides ready-to-use ML solutions. Classified finger joints of hand into 21 landmark positions, thus by manipulating the landmark points, made possible to virtually draw on air.

![image](https://user-images.githubusercontent.com/53861812/172015354-7be62537-913f-4656-a54b-a69d1224c073.png)

# Handwritten Text Recognition

Used Neural Networks (NN) to recognize the text written on air. Used IAM dataset for training the model. Model was trained using Convolutional Neural Network (CNN) and Recurrent Neural Network (RNN). 
5 layers of CNN were used and 2 layers of RNN were used. LSTM of RNN was used to train the model. A Connectionist Temporal Classification (CTC) was used to decode and find loss value of trained texts.
The recognized text was projected on user's screens and the text was uploaded to Firebase.

![image](https://user-images.githubusercontent.com/53861812/172015674-28c5ed49-bd56-457b-be90-d7a225113697.png)


# AR Application

Developed AR application which would read the text from Firebase and project the corresponding text on a user's AR environment.

![image](https://user-images.githubusercontent.com/53861812/172015770-13932b8c-3df2-4039-be05-903a36c98be0.png)

![image](https://user-images.githubusercontent.com/53861812/172015762-153fcb80-72a5-4590-b78e-07f38d4389d3.png)


# Program Execution

To run the program, clone the entire repository. Install the packages in requirements.txt and run air_draw.py. Use the index finger to draw, index and middle finger to erase and open palm to clear any drawings. Use the pinky finger (finger up) only to send the drawn text to the deep learning model and predict the text. The predicted text is uploaded into Firebase from where the AR application loads the text.

The directory Air_Board is for the AR application. No need of this directory for writing and prediction purposes.
The directory model contains the snapshots of the trained model with which the text is predicted upon.

In firebase_uploader.py, use your own Firebase storage bucket and apiKey. Also create a new serviceAccountKey.json file for the private keys and other related information. Refer the video below for more information

[![Watch the video](https://i.ytimg.com/an_webp/gLyaR3KPYt4/mqdefault_6s.webp?du=3000&sqp=CNCugZYG&rs=AOn4CLDY4abUCT-B_vUh4XkxOzJjqBtRdA)](https://www.youtube.com/watch?v=gLyaR3KPYt4)
