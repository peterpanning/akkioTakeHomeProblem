# akkioTakeHomeProblem
This project was set up with pdm, a new (to me) python dependency manager. It uses python 3.9 and one (1) library, the 
Python Image Library, to generate identicons.

pdm created a .venv for the project which includes both the required python version and this library, so you shouldn't 
need to install anything assuming you correctly load that .venv

Run it in an interpreter: 

>>> from src.akkiotakehomeproblem.identicon import generate_identicon
>>> i = generate_identicon('akkio')
>>> i.show()

Let me know if you run into any issues, want to discuss implementation choices made, etc 