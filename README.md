# Login Seguro - TecnoMarket

Este proyecto implementa un módulo de login seguro para el caso TecnoMarket.

## Requisitos implementados

- Formulario HTML con método POST.
- Despliegue preparado para HTTPS mediante Render.
- Validación de entradas del usuario.
- Consultas SQL parametrizadas.
- Contraseñas almacenadas con hash seguro y sal.
- Mensaje de error genérico ante credenciales inválidas.
- Control básico contra fuerza bruta.
- Separación entre lógica, validación y respuesta al usuario.

## Ejecución local

```bash
pip install -r requirements.txt
python crear_bd.py
python crearusuarios.py
python app.py