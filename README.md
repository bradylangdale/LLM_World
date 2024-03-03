# LLM_World
Create a 2D GUI to watch a local LLM explore a 2D world. The 2D graphics are based on (AggiEngine)[https://github.com/aggie-coding-club/AggiEngine].

# Screenshots
The following image displays what the LLM is prompted.

While the user is able to watch the LLM move in a more theme environment.

# Local LLMs
This project relies on Oobabooga for hosting the local LLM and providing an API to it. `oobabooga.py` acts as the bridge between Oobabooga and the Python instance. Inheriting `llm.py` enables a user to utilizes multiple LLMs by telling Oobabooga to switch out the model at runtime, however this is not utilized in this project.
