#!/usr/bin/env python3
import sys, io, json, traceback

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data.strip():
            raise ValueError("No se recibió ningún dato en stdin")

        data = json.loads(input_data)
        code = data.get('code', '')
        if not code:
            raise ValueError("No se proporcionó código en el campo 'code'")

        # Variables inyectadas disponibles en el contexto del código
        exec_globals = {k: v for k, v in data.items() if k != 'code'}
        exec_locals  = {}

        stdout_capture = io.StringIO()
        sys.stdout = stdout_capture

        exec(code, exec_globals, exec_locals)

        sys.stdout = sys.__stdout__
        output = stdout_capture.getvalue()

        print(json.dumps({
            "success": True,
            "result": exec_locals.get('result', None),
            "output": output
        }, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        sys.stdout = sys.__stdout__
        print(json.dumps({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }, ensure_ascii=False))
        sys.exit(1)

if __name__ == '__main__':
    main()
