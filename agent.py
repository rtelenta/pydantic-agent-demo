from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.providers.bedrock import BedrockProvider

import logfire
from dotenv import load_dotenv
import os

load_dotenv()
logfire.configure(token=os.getenv('LOGFIRE_TOKEN'))

model = BedrockConverseModel(
    'us.anthropic.claude-3-5-haiku-20241022-v1:0',
    provider=BedrockProvider(
        region_name='us-east-1',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    ),
)

postgres_server = MCPServerStdio('npx', [
        "-y",
        "@modelcontextprotocol/server-postgres",
        os.getenv("DATABASE_URL")
      ])

agent = Agent(model, 
                instrument=True,
                mcp_servers=[postgres_server])


async def main():
    async with agent.run_mcp_servers():
        result = await agent.run("hola")
        while True:
            print(f"\n{result.output}")
            user_input = input("\n> ")
            result = await agent.run(user_input, message_history=result.new_messages())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())