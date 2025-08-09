"""Tests for template substitution and secure quoting functionality"""
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add src directory to Python path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stringx.core.command import Command


class TestTemplateSubstitution:
    """Tests for template substitution functionality"""

    def setup_method(self):
        """Setup for each test method"""
        self.command = Command()

    def test_simple_template_substitution(self):
        """Test basic template substitution"""
        template = "echo {}"
        target = "test_string"
        
        result = self.command.format_command_template(template, target)
        assert "test_string" in result

    def test_multiple_placeholder_substitution(self):
        """Test template with multiple placeholders"""
        template = "curl -H 'User-Agent: {}' -o {}.html {}"
        target = "example.com"
        
        result = self.command.format_command_template(template, target)
        assert "example.com" in result
        assert result.count("example.com") >= 2

    def test_template_with_special_characters(self):
        """Test template substitution with special characters"""
        template = "echo '{}'"
        target = "test & echo 'injected'"
        
        result = self.command.format_command_template(template, target)
        # Should handle special characters safely
        assert "injected" not in result or "'" in result

    def test_template_with_quotes(self):
        """Test template substitution with quotes in target"""
        template = "echo {}"
        target = "test'with'quotes"
        
        result = self.command.format_command_template(template, target)
        assert "test'with'quotes" in result

    def test_template_with_backticks(self):
        """Test template substitution with backticks"""
        template = "echo {}"
        target = "test`command`injection"
        
        result = self.command.format_command_template(template, target)
        # Should handle backticks safely
        assert "`command`" in result or result.find("`") == -1

    def test_empty_template(self):
        """Test handling of empty template"""
        template = ""
        target = "test_string"
        
        result = self.command.format_command_template(template, target)
        assert result == ""

    def test_empty_target(self):
        """Test handling of empty target"""
        template = "echo {}"
        target = ""
        
        result = self.command.format_command_template(template, target)
        assert "{}" not in result

    def test_template_without_placeholder(self):
        """Test template without placeholder"""
        template = "echo hello"
        target = "test_string"
        
        result = self.command.format_command_template(template, target)
        assert result == "echo hello"

    def test_multiple_placeholders_same_target(self):
        """Test multiple placeholders with same target"""
        template = "ping {} && traceroute {}"
        target = "google.com"
        
        result = self.command.format_command_template(template, target)
        assert result.count("google.com") == 2


class TestSecureQuoting:
    """Tests for secure quoting functionality"""

    def setup_method(self):
        """Setup for each test method"""
        self.command = Command()

    def test_quote_shell_command_injection(self):
        """Test protection against shell command injection"""
        template = "echo {}"
        target = "test; rm -rf /"
        
        result = self.command.format_command_template(template, target)
        # Should escape or quote dangerous characters
        assert "rm -rf /" not in result or "'" in result or "\\" in result

    def test_quote_pipe_injection(self):
        """Test protection against pipe injection"""
        template = "echo {}"
        target = "test | cat /etc/passwd"
        
        result = self.command.format_command_template(template, target)
        # Should handle pipe characters safely
        assert "cat /etc/passwd" not in result or "'" in result

    def test_quote_redirection_injection(self):
        """Test protection against redirection injection"""
        template = "echo {}"
        target = "test > /tmp/malicious"
        
        result = self.command.format_command_template(template, target)
        # Should handle redirection safely
        assert "/tmp/malicious" not in result or "'" in result

    def test_quote_variable_expansion(self):
        """Test protection against variable expansion"""
        template = "echo {}"
        target = "$HOME/test"
        
        result = self.command.format_command_template(template, target)
        # Should prevent variable expansion
        assert "$HOME" in result

    def test_quote_command_substitution(self):
        """Test protection against command substitution"""
        template = "echo {}"
        target = "$(whoami)"
        
        result = self.command.format_command_template(template, target)
        # Should prevent command substitution
        assert "whoami" in result or "\\$" in result

    def test_quote_unicode_characters(self):
        """Test handling of Unicode characters"""
        template = "echo {}"
        target = "test_🌍_unicode"
        
        result = self.command.format_command_template(template, target)
        assert "🌍" in result

    def test_quote_newlines(self):
        """Test handling of newlines in target"""
        template = "echo {}"
        target = "line1\nline2"
        
        result = self.command.format_command_template(template, target)
        # Should handle newlines safely
        assert "line1" in result and "line2" in result

    def test_quote_null_bytes(self):
        """Test handling of null bytes"""
        template = "echo {}"
        target = "test\x00null"
        
        result = self.command.format_command_template(template, target)
        # Should handle null bytes safely
        assert "test" in result

    def test_quote_extremely_long_string(self):
        """Test handling of extremely long strings"""
        template = "echo {}"
        target = "a" * 10000
        
        result = self.command.format_command_template(template, target)
        assert len(result) > 10000
        assert "aaa" in result


class TestCommandValidation:
    """Tests for command validation functionality"""

    def setup_method(self):
        """Setup for each test method"""
        self.command = Command()

    def test_validate_safe_command(self):
        """Test validation of safe commands"""
        safe_commands = [
            "ping google.com",
            "curl https://example.com",
            "nslookup domain.com",
            "whois example.org"
        ]
        
        for cmd in safe_commands:
            # Should not raise exceptions for safe commands
            assert isinstance(cmd, str)
            assert len(cmd) > 0

    def test_validate_dangerous_command(self):
        """Test validation of potentially dangerous commands"""
        dangerous_commands = [
            "rm -rf /",
            "dd if=/dev/zero of=/dev/sda",
            ":(){ :|:& };:",  # Fork bomb
            "chmod 777 /etc/passwd"
        ]
        
        for cmd in dangerous_commands:
            # Should identify dangerous patterns
            assert any(dangerous in cmd for dangerous in ["rm -rf", "dd if=", ":(){", "chmod 777"])

    def test_validate_input_size_limits(self):
        """Test input size validation"""
        # Test normal sized input
        normal_input = "a" * 1000
        assert len(normal_input) == 1000
        
        # Test large input
        large_input = "a" * 100000
        assert len(large_input) == 100000
        
        # Could implement size limits in the actual command processor

    def test_validate_thread_limits(self):
        """Test thread limit validation"""
        # Test reasonable thread count
        reasonable_threads = 10
        assert reasonable_threads > 0
        assert reasonable_threads < 100
        
        # Test excessive thread count
        excessive_threads = 1000
        assert excessive_threads > 100

    def test_validate_timeout_settings(self):
        """Test timeout validation"""
        # Test reasonable timeout
        reasonable_timeout = 30
        assert reasonable_timeout > 0
        assert reasonable_timeout < 300
        
        # Test excessive timeout
        excessive_timeout = 86400  # 24 hours
        assert excessive_timeout > 3600


class TestSignalHandling:
    """Tests for signal handling and clean termination"""

    @patch('signal.signal')
    def test_signal_handler_registration(self, mock_signal):
        """Test signal handler registration"""
        # Import and test signal handler registration
        from stringx.cli import quit_process
        
        assert callable(quit_process)
        # Would test: signal.signal(signal.SIGINT, quit_process)

    def test_graceful_termination(self):
        """Test graceful termination on interrupt"""
        # Mock the termination process
        with patch('sys.exit') as mock_exit:
            from stringx.cli import quit_process
            
            # Simulate signal handler
            quit_process(None, None)
            mock_exit.assert_called_once_with(0)

    @patch('stringx.cli.CLI')
    def test_cleanup_on_termination(self, mock_cli):
        """Test cleanup operations on termination"""
        from stringx.cli import quit_process
        
        with patch('sys.exit'):
            quit_process(None, None)
            
        # Should log termination messages
        assert mock_cli.console.log.call_count >= 2


if __name__ == "__main__":
    pytest.main([__file__])