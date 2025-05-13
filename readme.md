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
git clone https://github.com/rtelenta/pydantic-agent-demo
cd pydantic-agent-demo
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
#ejectuar api con bedrock
uvicorn main:app --reload
```

```bash
#ejecutar en terminal con bedrock
python agent.py
```

```bash
#ejecutar api con groq
#para este ejemplo solo es necesario tener la key env GROQ_API_KEY
uvicorn agent_groq:app --reload
```

🧪 Ejemplo de uso

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "¿Qué juguetes para perros tienes?"}'
```
