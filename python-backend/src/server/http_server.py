import logging
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import base64
import numpy as np
import cv2
import tensorflow as tf

INTERPRETER = None
INPUT_DETAILS = None
OUTPUT_DETAILS = None
CLASS_NAMES = []

class PredictionHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
    def do_GET(self):
        if self.path == '/health':
            self._set_headers()
            response = {
                'status': 'ok',
                'model': 'loaded' if INTERPRETER else 'not_loaded',
                'classes': CLASS_NAMES
            }
            self.wfile.write(json.dumps(response).encode())
            
    def do_POST(self):
        if self.path == '/predict':
            try:
                content_length = int(self.headers['Content-Length'])
                data = json.loads(self.rfile.read(content_length))
                
                # Decodificar imagen
                image_data = data['image'].split(',')[1]
                image_bytes = base64.b64decode(image_data)
                image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
                
                # Preprocesar imagen
                image = cv2.resize(image, (200, 200))
                image = image / 255.0
                # TFLite requiere el tipo de dato float32
                image = np.expand_dims(image, axis=0).astype(np.float32)
                
                # Predicción con TFLite
                INTERPRETER.set_tensor(INPUT_DETAILS[0]['index'], image)
                INTERPRETER.invoke()
                predictions = INTERPRETER.get_tensor(OUTPUT_DETAILS[0]['index'])
                
                predicted_class = int(np.argmax(predictions[0]))
                confidence = float(predictions[0][predicted_class])
                
                response = {
                    'success': True,
                    'prediction': CLASS_NAMES[predicted_class],
                    'confidence': confidence,
                    'probabilities': {
                        CLASS_NAMES[i]: float(predictions[0][i])
                        for i in range(len(CLASS_NAMES))
                    }
                }
                
                self._set_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': str(e)}).encode())
                
    def log_message(self, format, *args):
        pass

def start_server(model_path, static_path, port):
    global INTERPRETER, INPUT_DETAILS, OUTPUT_DETAILS, CLASS_NAMES
    
    logging.info(f"Cargando modelo TFLite: {model_path}")
    
    # Cargar modelo TFLite e inicializar tensores
    INTERPRETER = tf.lite.Interpreter(model_path=model_path)
    INTERPRETER.allocate_tensors()
    INPUT_DETAILS = INTERPRETER.get_input_details()
    OUTPUT_DETAILS = INTERPRETER.get_output_details()
    
    # IMPORTANTE: Cambia esto por las letras de lenguaje de señas que reconoce tu modelo
    CLASS_NAMES = ['A', 'B', 'C'] 
    
    logging.info(f"✅ Servidor iniciado en http://127.0.0.1:{port}")
    
    server = HTTPServer(('127.0.0.1', port), PredictionHandler)
    server.serve_forever()