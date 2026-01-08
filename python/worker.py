#!/usr/bin/env python3
import sys
import io
import json
import traceback

def main():
    try:
        input_data = sys.stdin.read()
        
        if not input_data.strip():
            raise ValueError("No input data")
        
        data = json.loads(input_data)
        code = data.get('code', '')
        clientes = data.get('clientes', [])
        
        if not code:
            raise ValueError("No code provided")
        
        stdout_capture = io.StringIO()
        sys.stdout = stdout_capture
        
        exec_globals = {'clientes': clientes}
        exec_locals = {}
        
        exec(code, exec_globals, exec_locals)
        
        sys.stdout = sys.__stdout__
        output = stdout_capture.getvalue()
        
        result = exec_locals.get('result', None)
        
        response = {
            "success": True,
            "result": result,
            "output": output
        }
        
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