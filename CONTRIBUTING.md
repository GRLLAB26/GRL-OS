# Contributing

Gracias por querer contribuir a GRL-OS. Para mantener un flujo de trabajo claro, sigue estos pasos básicos.

1. Haz fork del repositorio y crea una rama para tu trabajo:

```bash
git checkout -b feat/mi-nueva-funcionalidad
```

2. Escribe pruebas que cubran la nueva funcionalidad cuando sea posible.

3. Asegúrate de que las pruebas y el estilo pasen:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest
```

4. Haz commits claros y atómicos.

5. Empuja la rama a tu fork y abre un Pull Request hacia `main` explicando los cambios.

6. Sigue las indicaciones de revisión, actualiza el PR y espera la aprobación.

Si tienes dudas sobre la dirección del proyecto, abre una issue para discutir la propuesta antes de implementar.
