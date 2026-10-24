"""One real local MCP stdio call; uses the installed package, no model or API."""
import asyncio
import json
import os
import sys
from mcp import Client, StdioServerParameters

PARAMETERS = {
    "test": "t2-indep", "mode": "a-priori", "tails": 2,
    "d": 0.5, "alpha": 0.05, "power": 0.95, "ratio": 1,
}

async def calculate():
    env = {key: value for key, value in os.environ.items()
           if key.upper() in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP")}
    env["PYTHONIOENCODING"] = "utf-8"
    server = StdioServerParameters(
        command=sys.executable,
        args=["-I", "-m", "independent_t.mcp_server"], env=env,
    )
    async with Client(server, read_timeout_seconds=12, mode="legacy") as client:
        tools = await client.list_tools()
        if [tool.name for tool in tools.tools] != ["power_analysis"]:
            raise RuntimeError("Unexpected installed MCP tool inventory")
        response = await client.call_tool("power_analysis", PARAMETERS)
        if response.is_error or len(response.content) != 1:
            raise RuntimeError("MCP did not return one successful text result")
        text = response.content[0].text
        result = json.loads(text)
        if result != response.structured_content:
            raise RuntimeError("MCP text and structured payload differ")
        if [result.get(key) for key in ("n1", "n2", "n_total")] != [105, 105, 210]:
            raise RuntimeError("Unexpected MCP allocation")
        # Emit the actual server text, not a reconstructed sample answer.
        print(text, flush=True)

if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(calculate(), timeout=15))
