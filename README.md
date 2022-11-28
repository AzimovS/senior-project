<h3 align="center">Football Action Classification</h3>

This project is a part of a larger system that aims to improve the experience of the audience received by the football content. We developed a desktop application that allows users to interact with the ML and DL algorithms that train, visualize and predict football actions on provided data. In the last semester, we worked on the improvement of the algorithms and the quality of desktop application functionalities. For instance, tested other deep learning models, such as DenseNet and VGG for image classification, added hotkeys for the visualization page, etc. We also implemented the best model to our Desktop app on the Prediction page, changed the visualization part from correct/incorrect to annotation by action and test the desktop application for bugs

## About the project

Here you can see the diagram of thw software.

![image](https://user-images.githubusercontent.com/35425540/204219890-4dc77f9a-3d88-476d-a41d-8581904d51ec.png)

This is how the application looks after initial launch.
![image](https://user-images.githubusercontent.com/35425540/204221583-75c66752-0016-4c40-9d98-dfda54911c8b.png)

Here is the most important features of the application:

   1. Video visualization and labelling
![image](https://user-images.githubusercontent.com/35425540/204221959-995c60d8-d9bd-46c3-b92b-46dc3051d168.png)

   2. Visualization of the training models
![image](https://user-images.githubusercontent.com/35425540/204222242-3eb5c303-3842-4dfd-bf7c-8392c8d4f4d8.png)


## Getting started

Create a new environment with conda (or any other). The python version is 3.8
	conda create -n lfc_verification python=3.8

1. Install all libraries from requirements.txt with

   ```sh
   pip install -r requirements.txt
   ```
2. Start the app
   ```sh
   python main.py
   ```
   

## Built With

* [PyQt](https://riverbankcomputing.com/software/pyqt/)
* [PyTorch](https://github.com/pytorch)
* [OpenCV](https://github.com/opencv/opencv)
* [Scikit-learn](https://github.com/scikit-learn/scikit-learn)

## Developed by

* [Bekzat Manapov](https://github.com/bexxman)
* [Sherkhan Azimov](https://github.com/azimovs)
