# GRL-OS

GRL-OS es el repositorio base para el proyecto GRL. Contiene utilidades, una pequeña interfaz opcional con `customtkinter` y los servicios iniciales del proyecto.

## Requisitos

- Python 3.11+ (probado con 3.13)
- Ver `requirements.txt` para las dependencias del proyecto.

## Inicio rápido

1. Crear y activar un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
.venv/bin/python -m pip install --upgrade pip setuptools wheel
.venv/bin/python -m pip install -r requirements.txt
```

3. Ejecutar la aplicación (modo CLI):

```bash
.venv/bin/python main.py
```

O iniciar la GUI (si estás en un entorno con soporte gráfico):

```bash
.venv/bin/python main.py --gui
```

## Desarrollo

- Ejecutar pruebas:

```bash
.venv/bin/python -m pytest
```

- Formato y lint: añade herramientas según prefieras (black, ruff, etc.).

## Contribuir

1. Crea una rama por funcionalidad: `git checkout -b feat/mi-nueva-funcionalidad`
2. Añade pruebas y documentación mínima.
3. Haz commit y push, luego abre un Pull Request en GitHub.

## Licencia

Por definir. Añade un `LICENSE` cuando desees establecerla.

---

Si quieres, puedo añadir más secciones (arquitectura, instrucciones de despliegue, badges CI). Dime qué prefieres.
# GRL-OS