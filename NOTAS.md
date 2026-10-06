# Estado de la modernizacion (rama modernizar)

- main: version funcionando (Python 3.11, TensorFlow 2.13, Electron 28).
- http_server.py ya usa ai_edge_litert (LiteRT) en lugar de tensorflow.
- Pendiente: confirmar con test_all.py que las clases coinciden con la version TensorFlow.
- Pendiente: CLASS_NAMES es provisional (indices 0-15); hipotesis A-Q sin J, sin confirmar.
- Pendiente: main.js sigue apuntando a venv; requirements.txt sigue con TensorFlow.
- Entorno ligero: py -3.11 -m venv venv-lite ; python -m pip install -r python-backend/requirements-litert.txt
- Si pip.exe esta bloqueado, usar siempre: python -m pip
