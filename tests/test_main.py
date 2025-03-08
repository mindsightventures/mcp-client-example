import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_client.__main__ import main


@pytest.mark.asyncio
async def test_main():
    """Test the main function"""
    # Mock the sys.argv
    with patch.object(sys, "argv", ["mcp_client", "test_server.py"]):
        # Mock the MCPClient class
        with patch("mcp_client.__main__.MCPClient") as mock_client_class:
            # Create a mock client instance
            mock_client = MagicMock()
            mock_client.connect_to_server = AsyncMock()
            mock_client.chat_loop = AsyncMock()
            mock_client.cleanup = AsyncMock()

            # Make the mock class return our mock instance
            mock_client_class.return_value = mock_client

            # Call the main function
            await main()

            # Verify the client methods were called in the right order
            mock_client_class.assert_called_once()
            mock_client.connect_to_server.assert_called_once_with("test_server.py")
            mock_client.chat_loop.assert_called_once()
            mock_client.cleanup.assert_called_once()


@pytest.mark.asyncio
async def test_main_no_args():
    """Test the main function with no arguments"""
    # Mock the sys.argv and sys.exit
    with (
        patch.object(sys, "argv", ["mcp_client"]),
        patch("mcp_client.__main__.sys.exit", side_effect=SystemExit) as mock_exit,
    ):

        try:
            # Call the main function
            await main()
        except SystemExit:
            pass  # Expected behavior

        # Verify sys.exit was called with code 1
        mock_exit.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_main_exception():
    """Test the main function with an exception"""
    # Mock the sys.argv
    with patch.object(sys, "argv", ["mcp_client", "test_server.py"]):
        # Mock the MCPClient class
        with patch("mcp_client.__main__.MCPClient") as mock_client_class:
            # Create a mock client instance
            mock_client = MagicMock()
            mock_client.connect_to_server = AsyncMock(side_effect=Exception("Test error"))
            mock_client.cleanup = AsyncMock()

            # Make the mock class return our mock instance
            mock_client_class.return_value = mock_client

            # Call the main function - it should handle the exception
            await main()

            # Verify the client methods were called in the right order
            mock_client_class.assert_called_once()
            mock_client.connect_to_server.assert_called_once_with("test_server.py")
            mock_client.cleanup.assert_called_once()
