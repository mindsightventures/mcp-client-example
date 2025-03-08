import asyncio
import sys
from typing import NoReturn, Optional

from .client import MCPClient


async def main() -> Optional[NoReturn]:
    if len(sys.argv) < 2:
        print("Usage: python -m mcp_client <path_to_server_script>")
        sys.exit(1)
        # Return early for testing purposes
        return None

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await client.cleanup()

    return None


if __name__ == "__main__":
    asyncio.run(main())
