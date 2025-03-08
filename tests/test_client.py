from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_client.client import MCPClient


@pytest.fixture
def mcp_client():
    """Create a client with mocked dependencies for testing"""
    client = MCPClient()
    client.session = AsyncMock()
    client.stdio = MagicMock()
    client.write = AsyncMock()
    client.anthropic = MagicMock()
    return client


class TestMCPClient:
    def test_init(self):
        """Test client initialization"""
        client = MCPClient()
        assert client.session is None
        assert client.stdio is None
        assert client.write is None
        assert client.exit_stack is not None
        assert client.anthropic is not None

    @pytest.mark.asyncio
    async def test_connect_to_server_python(self, monkeypatch):
        """Test connecting to a Python server"""
        # Mock the necessary async context managers
        mock_stdio_client = AsyncMock()
        mock_stdio_client.return_value = (MagicMock(), AsyncMock())

        mock_client_session = AsyncMock()
        mock_session = AsyncMock()
        mock_client_session.return_value = mock_session

        # Create a client with a mocked exit_stack
        client = MCPClient()
        client.exit_stack.enter_async_context = AsyncMock()
        client.exit_stack.enter_async_context.side_effect = [
            (MagicMock(), AsyncMock()),  # First call returns stdio transport
            mock_session,  # Second call returns session
        ]

        # Apply the mocks
        with (
            patch("mcp_client.client.stdio_client", mock_stdio_client),
            patch("mcp_client.client.ClientSession", mock_client_session),
            patch("mcp_client.client.StdioServerParameters") as mock_params,
        ):
            # Mock the StdioServerParameters
            mock_params.return_value = MagicMock()

            # Call the method
            await client.connect_to_server("test_server.py")

            # Verify the correct parameters were used
            mock_params.assert_called_once()
            args, kwargs = mock_params.call_args
            assert kwargs["command"] == "python"
            assert kwargs["args"] == ["test_server.py"]

    @pytest.mark.asyncio
    async def test_process_query(self, mcp_client):
        """Test processing a query with tool calls"""
        # Mock the list_tools response
        tool_response = MagicMock()
        tool_response.tools = [MagicMock(name="test_tool", description="Test tool", inputSchema={"type": "object"})]
        mcp_client.session.list_tools.return_value = tool_response

        # Mock the anthropic response
        text_content = MagicMock(type="text", text="Test response")
        mcp_client.anthropic.messages.create.return_value = MagicMock(content=[text_content])

        # Call the method
        result = await mcp_client.process_query("test query")

        # Verify the result
        assert "Test response" in result
        mcp_client.session.list_tools.assert_called_once()
        mcp_client.anthropic.messages.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_query_with_tool_use(self, mcp_client):
        """Test processing a query with tool calls that use tools"""
        # Mock the list_tools response
        tool_response = MagicMock()
        tool_response.tools = [MagicMock(name="test_tool", description="Test tool", inputSchema={"type": "object"})]
        mcp_client.session.list_tools.return_value = tool_response

        # Mock the tool call response
        tool_call_result = MagicMock()
        tool_call_result.content = "Tool result"
        mcp_client.session.call_tool.return_value = tool_call_result

        # Mock the anthropic responses
        # First response with tool use
        tool_use_content = MagicMock(type="tool_use", name="test_tool", input={"param": "value"}, id="tool1")
        # Make sure the name property returns a string, not a MagicMock
        tool_use_content.name = "test_tool"
        first_response = MagicMock(content=[tool_use_content])

        # Second response after tool use
        text_content = MagicMock(type="text", text="Final response")
        second_response = MagicMock(content=[text_content])

        # Set up the side effect for multiple calls
        mcp_client.anthropic.messages.create.side_effect = [first_response, second_response]

        # Call the method
        result = await mcp_client.process_query("test query with tool")

        # Verify the result contains the expected strings
        assert "test_tool" in result
        assert "param" in result
        assert "value" in result
        assert "Final response" in result
        mcp_client.session.list_tools.assert_called_once()
        assert mcp_client.anthropic.messages.create.call_count == 2
        mcp_client.session.call_tool.assert_called_once_with("test_tool", {"param": "value"})

    @pytest.mark.asyncio
    async def test_chat_loop(self, mcp_client, monkeypatch):
        """Test the chat loop"""
        # Mock the input function to return "test query" then "quit"
        inputs = ["test query", "quit"]
        monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))

        # Mock the process_query method
        mcp_client.process_query = AsyncMock(return_value="Processed response")

        # Call the method
        await mcp_client.chat_loop()

        # Verify the process_query was called once with the right argument
        mcp_client.process_query.assert_called_once_with("test query")

    @pytest.mark.asyncio
    async def test_chat_loop_error(self, mcp_client, monkeypatch):
        """Test the chat loop with an error"""
        # Mock the input function to return "test query" then "quit"
        inputs = ["test query", "quit"]
        monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))

        # Mock the process_query method to raise an exception
        mcp_client.process_query = AsyncMock(side_effect=Exception("Test error"))

        # Call the method (should not raise an exception)
        await mcp_client.chat_loop()

        # Verify the process_query was called once with the right argument
        mcp_client.process_query.assert_called_once_with("test query")

    @pytest.mark.asyncio
    async def test_cleanup(self, mcp_client):
        """Test the cleanup method"""
        # Mock the exit_stack.aclose method
        mcp_client.exit_stack.aclose = AsyncMock()

        # Call the method
        await mcp_client.cleanup()

        # Verify the exit_stack.aclose was called
        mcp_client.exit_stack.aclose.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_connect_to_server_js(self, monkeypatch):
        """Test connecting to a JavaScript server"""
        # Mock the necessary async context managers
        mock_stdio_client = AsyncMock()
        mock_stdio_client.return_value = (MagicMock(), AsyncMock())

        mock_client_session = AsyncMock()
        mock_session = AsyncMock()
        mock_client_session.return_value = mock_session

        # Create a client with a mocked exit_stack
        client = MCPClient()
        client.exit_stack.enter_async_context = AsyncMock()
        client.exit_stack.enter_async_context.side_effect = [
            (MagicMock(), AsyncMock()),  # First call returns stdio transport
            mock_session,  # Second call returns session
        ]

        # Apply the mocks
        with (
            patch("mcp_client.client.stdio_client", mock_stdio_client),
            patch("mcp_client.client.ClientSession", mock_client_session),
            patch("mcp_client.client.StdioServerParameters") as mock_params,
        ):
            # Mock the StdioServerParameters
            mock_params.return_value = MagicMock()

            # Call the method
            await client.connect_to_server("test_server.js")

            # Verify the correct parameters were used
            mock_params.assert_called_once()
            args, kwargs = mock_params.call_args
            assert kwargs["command"] == "node"
            assert kwargs["args"] == ["test_server.js"]

    @pytest.mark.asyncio
    async def test_connect_to_server_invalid(self):
        """Test connecting to an invalid server file"""
        client = MCPClient()

        # Verify that an invalid file extension raises a ValueError
        with pytest.raises(ValueError, match="Server script must be a .py or .js file"):
            await client.connect_to_server("invalid_file.txt")
