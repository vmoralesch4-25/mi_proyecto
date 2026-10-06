# Estado de la modernizacion (rama modernizar)

- main: version funcionando (Python 3.11, TensorFlow 2.13, Electron 28).
- http_server.py ya usa ai_edge_litert (LiteRT) en lugar de tensorflow.
- Pendiente: confirmar con test_all.py que las clases coinciden con la version TensorFlow.
- Pendiente: CLASS_NAMES es provisional (indices 0-15); hipotesis A-Q sin J, sin confirmar.
- Pendiente: main.js sigue apuntando a venv; requirements.txt sigue con TensorFlow.
- Entorno ligero: py -3.11 -m venv venv-lite ; python -m pip install -r python-backend/requirements-litert.txt
- Si pip.exe esta bloqueado, usar siempre: python -m pip

## Actualizacion
- CLASS_NAMES: orden A-Q sin J, confirmado en 14 de 16 clases; G (6) y N (12) por eliminacion. N.jpg se clasifica como E (0.51).
- referencia_tensorflow.txt: salida de test_all.py con TensorFlow. Para comparar: arrancar el servidor con venv-lite, correr 'python test_all.py > litert.txt' y 'fc.exe referencia_tensorflow.txt litert.txt'.
- La comparacion LiteRT vs TensorFlow sigue PENDIENTE.

## Actualizacion
- CLASS_NAMES: orden A-Q sin J, confirmado en 14 de 16 clases; G (6) y N (12) por eliminacion. N.jpg se clasifica como E (0.51).
- referencia_tensorflow.txt: salida de test_all.py con TensorFlow. Para comparar: servidor con venv-lite, 'python test_all.py > litert.txt' y 'fc.exe referencia_tensorflow.txt litert.txt'.
- La comparacion LiteRT vs TensorFlow sigue PENDIENTE.
