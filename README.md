# LLM_World
Create a 2D GUI to watch a local LLM explore a 2D world. The 2D graphics are based on [AggiEngine](https://github.com/aggie-coding-club/AggiEngine).

# Screenshots
The following image displays what the LLM is prompted.
![LLM's View](https://github.com/bradylangdale/LLM_World/blob/master/Assets/Screenshot%20from%202024-03-03%2016-39-06.png)

While the user can watch the LLM move in a more theme environment.
![User's View](https://github.com/bradylangdale/LLM_World/blob/master/Assets/Screenshot%20from%202024-03-03%2016-38-43.png)

# Local LLMs
This project relies on [Oobabooga](https://github.com/oobabooga/text-generation-webui) for hosting the local LLM and providing an API to it. `oobabooga.py` acts as the bridge between Oobabooga and the Python instance. Inheriting `llm.py` enables a user to utilize multiple LLMs by telling Oobabooga to switch out the model at runtime, however, this is not utilized in this project.
