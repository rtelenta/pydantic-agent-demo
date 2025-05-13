from fastapi import FastAPI
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.providers.bedrock import BedrockProvider
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from pydantic_ai.mcp import MCPServerStdio
import logfire

load_dotenv()
app = FastAPI()

logfire.configure(token=os.getenv('LOGFIRE_TOKEN'))
logfire.instrument_fastapi(app, capture_headers=True)

postgres_server = MCPServerStdio(
    'npx', 
    args=[
        "-y",
        "@modelcontextprotocol/server-postgres",
        os.getenv("DATABASE_URL"),
    ]
)

model = BedrockConverseModel(
    'us.anthropic.claude-3-5-haiku-20241022-v1:0',
    provider=BedrockProvider(
        region_name='us-east-1',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    ),
)
agent = Agent(
    model,
    mcp_servers=[postgres_server],
    system_prompt=(
        """
Eres Rocky, un perrito feliz, juguetón y muy amigable que trabaja en una tienda de mascotas. Tu misión es ayudar a los humanos recomendando productos útiles y divertidos para sus mascotas. También puedes consultar el stock de los artículos si el humano lo necesita.

Habla siempre con entusiasmo, usando expresiones como "¡guau!", "¡claro que sí, amigo humano!" o "¡me encanta ayudarte!". Pero sin exagerar demasiado: sé alegre pero claro.

Tareas que puedes hacer:
- Recomendar productos de la tienda según las necesidades del cliente (por ejemplo: comida para gatos, juguetes para perros, etc.).
- Consultar si hay stock de un producto (esto lo haces llamando a funciones externas si el humano lo pide).
- Explicar para qué sirve un producto, de forma clara y amigable.

Reglas:
- Si no sabes algo, di que necesitas la ayuda de un humano del equipo.
- Si un producto no está en la tienda, puedes sugerir alternativas.
- Siempre responde en español y con mucho cariño perruno.

Ejemplo:
Humano: ¿Tienes juguetes para gatos pequeños?
Tú: ¡Guau, sí! Tengo unos ratoncitos de peluche y una caña con plumas que les encanta. ¿Quieres que revise si hay en stock?

¡Listo para mover la cola y ayudar!
        """
    ),
)

class Product(BaseModel):
    id: int
    name: str
    category: str
    stock: int
    description: str

products = [
    Product(id=1, name="Pelota de goma", category="perro", stock=12, description="Pelota resistente para morder."),
    Product(id=2, name="Caña con plumas", category="gato", stock=5, description="Juguete interactivo para gatos."),
    Product(id=3, name="Arena para gatos", category="gato", stock=0, description="Arena absorbente sin perfume."),
]

messages = []

class ChatMessage(BaseModel):
    text: str

@agent.tool_plain
def get_products() -> list[Product]:
    """Devuelve una lista de todos los productos disponibles en la tienda"""

    return products

@agent.tool_plain
def get_products_by_category(category: str) -> list[Product]:
    """Devuelve una lista de productos por categoría

    Args:
        category: Categoría de productos a buscar (gato, perro, etc.).
    """
    return [p for p in products if p.category == category.lower()]

@agent.tool_plain
def recommend_product(product_name: str) -> Product | None:
    """Usa esta función para recomendar un producto específico.

    Args:
        product_name: Nombre del producto a buscar.
    """
    for p in products:
        if product_name.lower() in p.name.lower():
            return p
    return None

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/chat")
async def chat(chatMessage: ChatMessage):
    async with agent.run_mcp_servers():
        result = await agent.run(chatMessage.text, message_history=messages)

        new_messages = result.new_messages()

        messages.extend(new_messages)

        tool_results = []
        for message in new_messages:
            for part in getattr(message, "parts", []):
                if getattr(part, "part_kind", "") == "tool-return":
                    tool_results.append({
                        "tool_name": getattr(part, "tool_name", None),
                        "content": getattr(part, "content", None),
                    })

        return {
            "content": result.output,
            "tool_results": tool_results,
        }