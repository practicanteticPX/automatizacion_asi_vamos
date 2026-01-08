#!/usr/bin/env python3
"""
Python Worker - Ejecución efímera para n8n
Entrada: JSON vía stdin
Salida: JSON vía stdout
"""

import sys
import io
import json
import traceback

def main():
    try:
        # Leer entrada desde stdin
        input_data = sys.stdin.read()
        
        if not input_data.strip():
            raise ValueError("No se recibió ningún dato en stdin")
        
        # Parsear JSON
        data = json.loads(input_data)
        code = data.get('code', '')
        
        if not code:
            raise ValueError("No se proporcionó código Python en el campo 'code'")
        
        # Capturar stdout
        stdout_capture = io.StringIO()
        sys.stdout = stdout_capture
        
        # Entorno de ejecución
        exec_globals = {}
        exec_locals = {}
        
        # Ejecutar el código
        exec(code, exec_globals, exec_locals)
        
        # Restaurar stdout
        sys.stdout = sys.__stdout__
        output = stdout_capture.getvalue()
        
        # Obtener resultado
        execution_result = exec_locals.get('result', None)
        
        # Construir respuesta
        response = {
            "success": True,
            "result": execution_result,
            "output": output
        }
        
        # Imprimir como JSON en stdout
        print(json.dumps(response, ensure_ascii=False))
        sys.exit(0)
        
    except Exception as e:
        sys.stdout = sys.__stdout__
        error_response = {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(json.dumps(error_response, ensure_ascii=False))
        sys.exit(1)

if __name__ == '__main__':
    main()