# Mini_Proyect2_Interaction_System

## Team Members

- **Member 1**: Willian Chapid 
- **Member 2**: Esteban Llanos

**Delivery Date**: 22:00 - 05/09/2024

## Project Description

This project focuses on the development of a Zork-style game where the player progresses through the story by making decisions and consistently hearing sounds based on the chosen actions. The game offers an immersive experience where each decision triggers a unique audio effect, enhancing the storytelling and engagement.

## Justification

This project was developed in Python using the PyOpenAL library for handling 3D audio. The story unfolds line by line through the command line interface (CMD), playing sounds corresponding to the selected actions. 

Clean code principles were applied, and modules and resources were separated to improve code readability and maintainability. The story is loaded from a `.csv` file located in `resources/story`, where each row represents a storyline node with associated actions. These actions are executed dynamically, utilizing threads in `main.py` as needed to prevent interruptions in the narrative flow and to allow multiple sounds to be played simultaneously.

This structure enables smooth gameplay and a seamless integration of sound and story, making it an ideal project for developers interested in interactive storytelling and audio programming.

## Installation Steps

To set up the development environment for this project, follow these steps:
```bash
   git clone https://github.com/Wislian/Mini_Proyect2_Interaction_System.git

   cd Mini_Proyect2_Interaction_System

   python -m venv .venv
```

Windows
```bash
   .venv\Scripts\activate
```
Linux
```bash
   source .venv/Scripts/activate
```
install Dependencies
```bash
pip install -r requirements.txt
```
run
```bash
python main.py
```
Deactivate virtual Enviroment
```bash
deactivate
```