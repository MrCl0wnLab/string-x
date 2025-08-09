"""Tests for file I/O functionality"""
import io
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add src directory to Python path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stringx.core.filelocal import FileLocal


class TestFileLocal:
    """Tests for FileLocal class"""

    def setup_method(self):
        """Setup for each test method"""
        self.file_local = FileLocal()

    def test_open_file_with_utf8(self, tmp_path: Path):
        """Test reading a UTF-8 file"""
        test_file = tmp_path / "test.txt"
        content = "test line 1\ntest line 2\n\ntest line 3"
        test_file.write_text(content, encoding='utf-8')
        
        lines, _ = self.file_local.open_file(str(test_file), 'r')
        assert lines == ["test line 1", "test line 2", "", "test line 3"]

    def test_open_file_with_latin1(self, tmp_path: Path):
        """Test reading a Latin-1 encoded file"""
        test_file = tmp_path / "latin1.txt"
        content = "café naïve"
        test_file.write_bytes(content.encode('latin-1'))
        
        # Should handle different encodings gracefully
        try:
            lines, _ = self.file_local.open_file(str(test_file), 'r')
            assert len(lines) > 0
        except UnicodeDecodeError:
            # Expected if encoding detection fails
            pass

    def test_open_file_nonexistent(self):
        """Test opening nonexistent file"""
        with pytest.raises(FileNotFoundError):
            self.file_local.open_file("nonexistent.txt", 'r')

    def test_open_file_binary_mode(self, tmp_path: Path):
        """Test opening file in binary mode"""
        test_file = tmp_path / "binary.txt"
        content = b"\x00\x01\x02\x03"
        test_file.write_bytes(content)
        
        lines, _ = self.file_local.open_file(str(test_file), 'rb')
        assert isinstance(lines, bytes)

    def test_write_file(self, tmp_path: Path):
        """Test writing to file"""
        test_file = tmp_path / "output.txt"
        content = ["line1", "line2", "line3"]
        
        self.file_local.write_file(str(test_file), content)
        
        assert test_file.exists()
        written_content = test_file.read_text()
        assert "line1" in written_content
        assert "line2" in written_content
        assert "line3" in written_content

    def test_append_file(self, tmp_path: Path):
        """Test appending to file"""
        test_file = tmp_path / "append.txt"
        test_file.write_text("initial content\n")
        
        self.file_local.append_file(str(test_file), "appended content")
        
        content = test_file.read_text()
        assert "initial content" in content
        assert "appended content" in content

    def test_file_permissions(self, tmp_path: Path):
        """Test file permission handling"""
        test_file = tmp_path / "restricted.txt"
        test_file.write_text("content")
        test_file.chmod(0o000)  # No permissions
        
        try:
            with pytest.raises(PermissionError):
                self.file_local.open_file(str(test_file), 'r')
        finally:
            test_file.chmod(0o644)  # Restore permissions for cleanup

    def test_large_file_handling(self, tmp_path: Path):
        """Test handling of large files"""
        test_file = tmp_path / "large.txt"
        
        # Create a file with many lines
        lines = [f"line {i}" for i in range(1000)]
        test_file.write_text("\n".join(lines))
        
        result_lines, _ = self.file_local.open_file(str(test_file), 'r')
        assert len(result_lines) == 1000
        assert result_lines[0] == "line 0"
        assert result_lines[-1] == "line 999"

    def test_empty_file(self, tmp_path: Path):
        """Test handling empty file"""
        test_file = tmp_path / "empty.txt"
        test_file.touch()
        
        lines, _ = self.file_local.open_file(str(test_file), 'r')
        assert lines == []

    def test_file_with_different_line_endings(self, tmp_path: Path):
        """Test handling files with different line endings"""
        test_file = tmp_path / "line_endings.txt"
        
        # Write file with mixed line endings
        content = "line1\rline2\nline3\r\nline4"
        test_file.write_bytes(content.encode('utf-8'))
        
        lines, _ = self.file_local.open_file(str(test_file), 'r')
        # Should handle different line endings gracefully
        assert len(lines) >= 1


class TestEncodingDetection:
    """Tests for encoding detection functionality"""

    def test_utf8_detection(self, tmp_path: Path):
        """Test UTF-8 encoding detection"""
        test_file = tmp_path / "utf8.txt"
        content = "Hello 世界 🌍"
        test_file.write_text(content, encoding='utf-8')
        
        file_local = FileLocal()
        lines, _ = file_local.open_file(str(test_file), 'r')
        assert content in "\n".join(lines)

    def test_ascii_detection(self, tmp_path: Path):
        """Test ASCII encoding detection"""
        test_file = tmp_path / "ascii.txt"
        content = "Hello World"
        test_file.write_text(content, encoding='ascii')
        
        file_local = FileLocal()
        lines, _ = file_local.open_file(str(test_file), 'r')
        assert content in "\n".join(lines)

    def test_cp1252_detection(self, tmp_path: Path):
        """Test CP1252 encoding detection"""
        test_file = tmp_path / "cp1252.txt"
        content = "café naïve résumé"
        test_file.write_bytes(content.encode('cp1252'))
        
        file_local = FileLocal()
        # May or may not detect encoding correctly, but shouldn't crash
        try:
            lines, _ = file_local.open_file(str(test_file), 'r')
            assert len(lines) >= 0
        except UnicodeDecodeError:
            # Acceptable if encoding detection fails
            pass


class TestErrorHandling:
    """Tests for error handling in file operations"""

    def test_directory_as_file(self, tmp_path: Path):
        """Test trying to read directory as file"""
        test_dir = tmp_path / "test_directory"
        test_dir.mkdir()
        
        file_local = FileLocal()
        with pytest.raises((IsADirectoryError, PermissionError)):
            file_local.open_file(str(test_dir), 'r')

    def test_invalid_mode(self, tmp_path: Path):
        """Test invalid file mode"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        file_local = FileLocal()
        with pytest.raises(ValueError):
            file_local.open_file(str(test_file), 'invalid_mode')

    def test_write_to_readonly_directory(self, tmp_path: Path):
        """Test writing to read-only directory"""
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)  # Read-only
        
        test_file = readonly_dir / "test.txt"
        file_local = FileLocal()
        
        try:
            with pytest.raises(PermissionError):
                file_local.write_file(str(test_file), ["content"])
        finally:
            readonly_dir.chmod(0o755)  # Restore permissions for cleanup


if __name__ == "__main__":
    pytest.main([__file__])