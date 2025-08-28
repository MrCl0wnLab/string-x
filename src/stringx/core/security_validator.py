"""Security validation module for String-X

This module provides security validation and protection mechanisms
to prevent command injection, ensure safe input processing, and
validate system limits.
"""
import re
import shlex
import resource
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urlparse


class SecurityValidator:
    """Security validator for String-X operations"""

    # Maximum limits to prevent resource exhaustion (loaded from settings)
    from stringx.config import setting
    MAX_INPUT_SIZE = setting.STRX_MAX_INPUT_SIZE
    MAX_THREAD_COUNT = setting.STRX_MAX_THREAD_COUNT
    MAX_TIMEOUT = setting.STRX_MAX_TIMEOUT
    MAX_STRING_LIST_SIZE = setting.STRX_MAX_STRING_LIST_SIZE
    MAX_COMMAND_LENGTH = setting.STRX_MAX_COMMAND_LENGTH

    # Get patterns from configuration (with safe fallback)
    DANGEROUS_PATTERNS = getattr(setting, 'STRX_BLOCKED_COMMAND_PATTERNS', []) + [
        r'dd\s+if=',
        r'mkfs\.',
        r'fdisk',
        r'parted',
        r'passwd',
        r'chmod\s+777',
        r'chown\s+root',
        r'nc\s+.*-l',  # netcat listener
        r'ncat\s+.*-l',
        r'socat\s+',
        r'telnet\s+',
        r'ssh\s+',
        r'scp\s+',
        r'rsync\s+',
        r'wget\s+.*-O\s*/etc/',
        r'curl\s+.*-o\s*/etc/',
        r'python\s+-c\s+',
        r'perl\s+-e\s+',
        r'ruby\s+-e\s+',
        r'php\s+-r\s+',
        r'node\s+-e\s+',
        r'eval\s+',
        r'exec\s+',
        r':\(\)\{.*\}',  # Fork bomb pattern
        r'while\s+true',
        r'/proc/sys',
        r'/dev/mem',
        r'/dev/kmem',
        r'>/etc/',
        r'>>/etc/',
    ]

    # Safe commands whitelist - combine with allowed patterns from config
    SAFE_COMMANDS = {
        'ping', 'nslookup', 'dig', 'host', 'whois', 'curl', 'wget',
        'echo', 'printf', 'cat', 'head', 'tail', 'grep', 'awk', 'sed',
        'cut', 'sort', 'uniq', 'wc', 'find', 'ls', 'file', 'stat',
        'date', 'sleep', 'timeout', 'test', 'tr', 'base64', 'md5sum',
        'sha256sum', 'sha1sum', 'openssl'
    }

    @classmethod
    def validate_input_size(cls, data: Any) -> bool:
        """
        Validate input size to prevent resource exhaustion.
        
        Args:
            data: Input data to validate
            
        Returns:
            bool: True if size is within limits, False otherwise
        """
        try:
            if isinstance(data, str):
                return len(data.encode('utf-8')) <= cls.MAX_INPUT_SIZE
            elif isinstance(data, (list, tuple)):
                if len(data) > cls.MAX_STRING_LIST_SIZE:
                    return False
                total_size = sum(len(str(item).encode('utf-8')) for item in data)
                return total_size <= cls.MAX_INPUT_SIZE * len(data)
            elif isinstance(data, dict):
                total_size = sum(
                    len(str(k).encode('utf-8')) + len(str(v).encode('utf-8'))
                    for k, v in data.items()
                )
                return total_size <= cls.MAX_INPUT_SIZE
            else:
                return len(str(data).encode('utf-8')) <= cls.MAX_INPUT_SIZE
        except Exception:
            return False

    @classmethod
    def validate_thread_limits(cls, thread_count: int) -> bool:
        """
        Validate thread count limits.
        
        Args:
            thread_count: Number of threads to validate
            
        Returns:
            bool: True if within limits, False otherwise
        """
        return 1 <= thread_count <= cls.MAX_THREAD_COUNT

    @classmethod
    def validate_timeout(cls, timeout: int) -> bool:
        """
        Validate timeout values.
        
        Args:
            timeout: Timeout value in seconds
            
        Returns:
            bool: True if within limits, False otherwise
        """
        return 1 <= timeout <= cls.MAX_TIMEOUT

    @classmethod
    def sanitize_shell_input(cls, input_string: str) -> str:
        """
        Sanitize input string for shell command execution.
        
        Args:
            input_string: Input string to sanitize
            
        Returns:
            str: Sanitized string safe for shell execution
        """
        if not input_string:
            return ""
        
        # Remove null bytes
        sanitized = input_string.replace('\x00', '')
        
        # Remove control characters except newline and tab
        sanitized = ''.join(
            char for char in sanitized 
            if ord(char) >= 32 or char in '\n\t'
        )
        
        # Limit length
        if len(sanitized) > cls.MAX_COMMAND_LENGTH:
            sanitized = sanitized[:cls.MAX_COMMAND_LENGTH]
        
        return sanitized

    @classmethod
    def quote_shell_argument(cls, argument: str) -> str:
        """
        Safely quote shell arguments to prevent injection.
        
        Args:
            argument: Argument to quote
            
        Returns:
            str: Safely quoted argument
        """
        if not argument:
            return "''"
        
        # Use shlex.quote for proper shell escaping
        return shlex.quote(argument)

    @classmethod
    def validate_command_safety(cls, command: str) -> Tuple[bool, str]:
        """
        Validate if a command is safe to execute.
        
        Args:
            command: Command to validate
            
        Returns:
            Tuple[bool, str]: (is_safe, reason)
        """
        if not command or not command.strip():
            return False, "Empty command"
        
        command = command.strip()
        
        # Check command length
        if len(command) > cls.MAX_COMMAND_LENGTH:
            return False, f"Command too long (max {cls.MAX_COMMAND_LENGTH} chars)"
        
        # Check for dangerous patterns
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"Dangerous pattern detected: {pattern}"
        
        # Extract command name
        try:
            parts = shlex.split(command)
            if parts:
                cmd_name = parts[0].split('/')[-1]  # Remove path
                if cmd_name not in cls.SAFE_COMMANDS:
                    return False, f"Command not in safe list: {cmd_name}"
        except ValueError:
            return False, "Invalid command syntax"
        
        # Check for command injection patterns
        injection_patterns = [
            r';',      # Command separator
            r'\|',     # Pipe
            r'&',      # Background execution
            r'\$\(',   # Command substitution
            r'`',      # Command substitution
            r'>>?',    # Redirection
            r'<<',     # Here document
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, command):
                return False, f"Potential injection pattern: {pattern}"
        
        return True, "Command appears safe"

    @classmethod
    def validate_url_safety(cls, url: str) -> Tuple[bool, str]:
        """
        Validate URL for security concerns.
        
        Args:
            url: URL to validate
            
        Returns:
            Tuple[bool, str]: (is_safe, reason)
        """
        if not url:
            return False, "Empty URL"
        
        try:
            parsed = urlparse(url)
        except Exception as e:
            return False, f"Invalid URL format: {e}"
        
        # Check scheme
        if parsed.scheme not in ['http', 'https']:
            return False, f"Unsafe URL scheme: {parsed.scheme}"
        
        # Check for localhost/private IPs
        hostname = parsed.hostname
        if hostname:
            # Block localhost and private networks
            dangerous_hosts = [
                'localhost', '127.0.0.1', '::1',
                '0.0.0.0', '169.254.169.254'  # AWS metadata
            ]
            
            if hostname.lower() in dangerous_hosts:
                return False, f"Blocked hostname: {hostname}"
            
            # Check private IP ranges
            if cls._is_private_ip(hostname):
                return False, f"Private IP address: {hostname}"
        
        # Check URL length
        if len(url) > 2048:
            return False, "URL too long"
        
        return True, "URL appears safe"

    @classmethod
    def _is_private_ip(cls, hostname: str) -> bool:
        """Check if hostname is a private IP address"""
        try:
            import ipaddress
            ip = ipaddress.ip_address(hostname)
            return ip.is_private
        except ValueError:
            # Not a valid IP address
            return False

    @classmethod
    def validate_file_path(cls, file_path: str) -> Tuple[bool, str]:
        """
        Validate file path for security.
        
        Args:
            file_path: File path to validate
            
        Returns:
            Tuple[bool, str]: (is_safe, reason)
        """
        if not file_path:
            return False, "Empty file path"
        
        # Normalize path
        import os
        try:
            normalized = os.path.normpath(file_path)
        except Exception as e:
            return False, f"Invalid path: {e}"
        
        # Check for path traversal
        if '..' in normalized:
            return False, "Path traversal detected"
        
        # Check for dangerous paths
        dangerous_paths = [
            '/etc/', '/proc/', '/sys/', '/dev/', '/root/',
            '/boot/', '/usr/bin/', '/usr/sbin/', '/sbin/',
            '/bin/', '/var/run/', '/var/log/'
        ]
        
        for dangerous in dangerous_paths:
            if normalized.startswith(dangerous):
                return False, f"Access to dangerous path: {dangerous}"
        
        return True, "Path appears safe"

    @classmethod
    def check_system_resources(cls) -> Dict[str, Any]:
        """
        Check current system resource usage.
        
        Returns:
            Dict[str, Any]: System resource information
        """
        try:
            # Get memory usage
            mem_usage = resource.getrusage(resource.RUSAGE_SELF)
            
            return {
                'memory_peak_kb': mem_usage.ru_maxrss,
                'user_time': mem_usage.ru_utime,
                'system_time': mem_usage.ru_stime,
                'voluntary_context_switches': mem_usage.ru_nvcsw,
                'involuntary_context_switches': mem_usage.ru_nivcsw
            }
        except Exception as e:
            return {'error': str(e)}

    @classmethod
    def set_resource_limits(cls) -> bool:
        """
        Set system resource limits for security.
        
        Returns:
            bool: True if limits were set successfully
        """
        try:
            # Set CPU time limit (10 minutes)
            resource.setrlimit(resource.RLIMIT_CPU, (600, 600))
            
            # Set memory limit (1GB)
            resource.setrlimit(resource.RLIMIT_AS, (1024*1024*1024, 1024*1024*1024))
            
            # Set file size limit (100MB)
            resource.setrlimit(resource.RLIMIT_FSIZE, (100*1024*1024, 100*1024*1024))
            
            # Set maximum number of open files
            resource.setrlimit(resource.RLIMIT_NOFILE, (1024, 1024))
            
            return True
        except Exception:
            return False

    @classmethod
    def validate_regex_pattern(cls, pattern: str) -> Tuple[bool, str]:
        """
        Validate regex pattern for security (prevent ReDoS).
        
        Args:
            pattern: Regex pattern to validate
            
        Returns:
            Tuple[bool, str]: (is_safe, reason)
        """
        if not pattern:
            return False, "Empty pattern"
        
        # Check pattern length
        if len(pattern) > 1000:
            return False, "Pattern too long"
        
        # Check for catastrophic backtracking patterns
        dangerous_patterns = [
            r'\(\?\:\.\*\?\)\+',  # (.*)+ type patterns
            r'\(\.\*\)\+',        # (.*)+ patterns
            r'\(\.\+\)\+',        # (.+)+ patterns  
            r'\(\?\:\[\^\]\]\*\)\+',  # ([^]]*)+
        ]
        
        for dangerous in dangerous_patterns:
            if re.search(dangerous, pattern):
                return False, "Potentially dangerous regex pattern"
        
        # Test compilation
        try:
            re.compile(pattern)
        except re.error as e:
            return False, f"Invalid regex: {e}"
        
        return True, "Pattern appears safe"

    @classmethod
    def sanitize_log_output(cls, log_message: str) -> str:
        """
        Sanitize log output to prevent log injection.
        
        Args:
            log_message: Log message to sanitize
            
        Returns:
            str: Sanitized log message
        """
        if not log_message:
            return ""
        
        # Remove control characters and ensure single line
        sanitized = ''.join(
            char for char in log_message 
            if ord(char) >= 32 or char in ' \t'
        )
        
        # Replace newlines to prevent log injection
        sanitized = sanitized.replace('\n', ' ').replace('\r', ' ')
        
        # Limit length
        if len(sanitized) > 1000:
            sanitized = sanitized[:997] + "..."
        
        return sanitized

    @classmethod
    def validate_encoding(cls, data: bytes, max_size: int = None) -> Tuple[bool, str]:
        """
        Validate data encoding and size.
        
        Args:
            data: Data to validate
            max_size: Maximum allowed size in bytes
            
        Returns:
            Tuple[bool, str]: (is_valid, detected_encoding)
        """
        if max_size and len(data) > max_size:
            return False, "Data too large"
        
        # Try to detect encoding
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                data.decode(encoding)
                return True, encoding
            except UnicodeDecodeError:
                continue
        
        return False, "Unknown encoding"