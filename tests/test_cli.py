"""Tests for CLI functionality"""
import io
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

import pytest

# Add src directory to Python path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stringx.cli import stdin_get_list, open_file, main


class TestStdinGetList:
    """Tests for stdin_get_list function"""

    def test_stdin_utf8_encoding(self):
        """Test reading UTF-8 encoded stdin"""
        test_input = b"line1\nline2\n\nline3 \n"
        
        with patch('sys.stdin') as mock_stdin:
            mock_stdin.isatty.return_value = False
            mock_stdin.buffer.read.return_value = test_input
            
            result = stdin_get_list()
            assert result == ["line1", "line2", "line3"]

    def test_stdin_latin1_encoding(self):
        """Test reading Latin-1 encoded stdin"""
        test_input = "café naïve".encode('latin-1')
        
        with patch('sys.stdin') as mock_stdin:
            mock_stdin.isatty.return_value = False
            mock_stdin.buffer.read.return_value = test_input
            
            result = stdin_get_list()
            assert "café naïve" in result

    def test_stdin_empty_lines_filtered(self):
        """Test that empty lines are filtered out"""
        test_input = b"line1\n\n\nline2\n\n"
        
        with patch('sys.stdin') as mock_stdin:
            mock_stdin.isatty.return_value = False
            mock_stdin.buffer.read.return_value = test_input
            
            result = stdin_get_list()
            assert result == ["line1", "line2"]

    def test_stdin_is_tty(self):
        """Test handling when stdin is a terminal"""
        with patch('sys.stdin') as mock_stdin:
            mock_stdin.isatty.return_value = True
            
            result = stdin_get_list()
            assert result is None

    def test_stdin_keyboard_interrupt(self):
        """Test handling KeyboardInterrupt"""
        with patch('sys.stdin') as mock_stdin:
            mock_stdin.isatty.return_value = False
            mock_stdin.buffer.read.side_effect = KeyboardInterrupt()
            
            with patch('stringx.cli.CLI') as mock_cli:
                result = stdin_get_list()
                assert result is None
                mock_cli.console.print_exception.assert_called_once()


class TestOpenFile:
    """Tests for open_file function"""

    def setup_method(self):
        """Setup for each test method"""
        self.mock_file = MagicMock()
        
    @patch('stringx.cli.FILE')
    def test_open_file_success(self, mock_file_obj):
        """Test successful file opening"""
        mock_file_obj.open_file.return_value = (["line1", "line2"], None)
        
        result = open_file("test.txt")
        assert result == ["line1", "line2"]
        mock_file_obj.open_file.assert_called_once_with("test.txt", 'r')

    @patch('stringx.cli.FILE')
    def test_open_file_not_found(self, mock_file_obj):
        """Test file not found handling"""
        mock_file_obj.open_file.side_effect = FileNotFoundError("File not found")
        
        with patch('stringx.cli.CLI') as mock_cli:
            result = open_file("nonexistent.txt")
            assert result is None
            mock_cli.console.log.assert_called_once()

    @patch('stringx.cli.FILE')
    def test_open_file_permission_error(self, mock_file_obj):
        """Test permission denied handling"""
        mock_file_obj.open_file.side_effect = PermissionError("Permission denied")
        
        with patch('stringx.cli.CLI') as mock_cli:
            result = open_file("restricted.txt")
            assert result is None
            mock_cli.console.log.assert_called_once()

    @patch('stringx.cli.FILE')
    def test_open_file_unicode_decode_error(self, mock_file_obj):
        """Test Unicode decode error handling"""
        mock_file_obj.open_file.side_effect = UnicodeDecodeError(
            'utf-8', b'', 0, 1, 'invalid start byte'
        )
        
        with patch('stringx.cli.CLI') as mock_cli:
            result = open_file("invalid.txt")
            assert result is None
            mock_cli.console.log.assert_called_once()

    def test_open_file_empty_filename(self):
        """Test handling empty filename"""
        result = open_file("")
        assert result is None

        result = open_file(None)
        assert result is None


class TestMain:
    """Tests for main function"""

    @patch('stringx.cli.THREAD')
    @patch('stringx.cli.CMD')
    def test_main_with_valid_input(self, mock_cmd, mock_thread):
        """Test main function with valid input"""
        target_list = ["target1", "target2"]
        template_str = "echo {}"
        mock_args = MagicMock()
        
        main(target_list, template_str)
        
        mock_thread.exec_thread.assert_called_once_with(
            function_name=mock_cmd.command_template,
            command_str=template_str,
            target_list=target_list,
            argparse=mock_args,
        )

    @patch('stringx.cli.THREAD')
    @patch('stringx.cli.CMD')
    def test_main_with_empty_list(self, mock_cmd, mock_thread):
        """Test main function with empty target list"""
        target_list = []
        template_str = "echo {}"
        
        main(target_list, template_str)
        
        mock_thread.exec_thread.assert_not_called()

    @patch('stringx.cli.THREAD')
    @patch('stringx.cli.CMD')
    def test_main_with_empty_template(self, mock_cmd, mock_thread):
        """Test main function with empty template"""
        target_list = ["target1"]
        template_str = ""
        
        main(target_list, template_str)
        
        mock_thread.exec_thread.assert_not_called()

    @patch('stringx.cli.THREAD')
    @patch('stringx.cli.CMD')
    @patch('stringx.cli.CLI')
    def test_main_with_exception(self, mock_cli, mock_cmd, mock_thread):
        """Test main function exception handling"""
        target_list = ["target1"]
        template_str = "echo {}"
        mock_thread.exec_thread.side_effect = Exception("Test exception")
        
        main(target_list, template_str)
        
        mock_cli.console.print_exception.assert_called_once_with(max_frames=3)

    @patch('stringx.cli.THREAD')
    @patch('stringx.cli.CMD')
    @patch('stringx.cli.CLI')
    def test_main_with_broken_pipe_error(self, mock_cli, mock_cmd, mock_thread):
        """Test main function BrokenPipeError handling"""
        target_list = ["target1"]
        template_str = "echo {}"
        
        with patch.object(target_list, '__class__', list):
            mock_thread.exec_thread.side_effect = BrokenPipeError("Broken pipe")
            
            main(target_list, template_str)
            
            mock_cli.console.print_exception.assert_called_once_with(max_frames=3)

    def test_main_with_non_list_input(self):
        """Test main function with non-list input"""
        target_str = "not_a_list"
        template_str = "echo {}"
        
        # Should not raise exception, just return without processing
        main(target_str, template_str)


if __name__ == "__main__":
    pytest.main([__file__])
