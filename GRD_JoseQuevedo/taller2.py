#!/usr/bin/env python3
# Receta 1.7 – Manejar errores de socket correctamente (Python 3)
# Versión modernizada para Visual Studio Code

import sys
import socket
import argparse


def main():
    parser = argparse.ArgumentParser(description="Ejemplos de errores con sockets")
    parser.add_argument("--host", dest="host", required=True, help="Host remoto")
    parser.add_argument("--port", dest="port", type=int, required=True, help="Puerto")
    parser.add_argument("--file", dest="file", required=True, help="Archivo o recurso")
    args = parser.parse_args()

    host = args.host
    port = args.port
    filename = args.file

    # --- Primer bloque: crear socket ---
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"Error creando el socket: {e}")
        sys.exit(1)

    # --- Segundo bloque: conectar ---
    try:
        s.connect((host, port))
    except socket.gaierror as e:
        print(f"Error de dirección: {e}")
        sys.exit(1)
    except socket.error as e:
        print(f"Error de conexión: {e}")
        sys.exit(1)

    # --- Tercer bloque: enviar datos ---
    try:
        request = f"GET {filename} HTTP/1.0\r\n\r\n"
        s.sendall(request.encode())
    except socket.error as e:
        print(f"Error enviando datos: {e}")
        sys.exit(1)

    # --- Cuarto bloque: recibir datos ---
    while True:
        try:
            buffer = s.recv(2048)
        except socket.error as e:
            print(f"Error recibiendo datos: {e}")
            sys.exit(1)

        if not buffer:
            break

        sys.stdout.write(buffer.decode(errors="replace"))

    s.close()


if __name__ == "__main__":
    main()
