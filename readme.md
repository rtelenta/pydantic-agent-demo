# Pydantic agent demo

Este es un proyecto de demostración de un agente conversacional llamado **Rocky**, un perrito feliz que trabaja en una tienda de mascotas y ayuda a los humanos recomendando productos para animales.

## 🚀 Requisitos

- Python 3.11 o superior
- PostgreSQL en ejecución
- Variable de entorno `DATABASE_URL` configurada
- Entorno virtual con `venv` (opcional pero recomendado)
- `uvicorn` para correr el servidor

## 📦 Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/tu_usuario/firulais-agent.git
cd firulais-agent
```

2. Crea y activa un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

🏁 Ejecutar el servidor

```bash
uvicorn main:app --reload
```

o

```bash
python agent.py
```

🧪 Ejemplo de uso

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "¿Qué juguetes para perros tienes?"}'
```
