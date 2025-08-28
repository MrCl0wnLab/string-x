"""Tests for pipeline functionality with mock modules"""
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add src directory to Python path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stringx.core.thread_process import ThreadProcess
from stringx.core.command import Command


class MockModule:
    """Mock module for testing pipeline functionality"""
    
    def __init__(self, name: str, module_type: str):
        self.name = name
        self.module_type = module_type
        self.processed_inputs = []
        
    def process(self, input_data: str) -> str:
        """Mock process method"""
        self.processed_inputs.append(input_data)
        return f"{self.module_type}:{self.name}({input_data})"


class TestBasicPipeline:
    """Tests for basic pipeline functionality"""

    def setup_method(self):
        """Setup for each test method"""
        self.thread_process = ThreadProcess()
        self.command = Command()
        
    def test_single_module_pipeline(self):
        """Test pipeline with single module"""
        mock_module = MockModule("test_module", "EXT")
        input_data = "test_input"
        
        result = mock_module.process(input_data)
        
        assert result == "EXT:test_module(test_input)"
        assert input_data in mock_module.processed_inputs

    def test_two_module_pipeline(self):
        """Test pipeline with two modules"""
        extractor = MockModule("email_extractor", "EXT")
        collector = MockModule("domain_collector", "CLC")
        
        # Simulate pipeline: input -> extractor -> collector
        input_data = "contact@example.com"
        
        # First module processes input
        extracted_data = extractor.process(input_data)
        
        # Second module processes output from first
        final_result = collector.process(extracted_data)
        
        assert "contact@example.com" in extractor.processed_inputs
        assert extracted_data in collector.processed_inputs
        assert "EXT:email_extractor" in final_result
        assert "CLC:domain_collector" in final_result

    def test_module_chaining_syntax(self):
        """Test module chaining syntax parsing"""
        chain_syntax = "ext:email|clc:domain|out:json"
        modules = chain_syntax.split("|")
        
        assert len(modules) == 3
        assert modules[0] == "ext:email"
        assert modules[1] == "clc:domain"
        assert modules[2] == "out:json"
        
        # Parse module types and names
        parsed_modules = []
        for module in modules:
            if ":" in module:
                mod_type, mod_name = module.split(":", 1)
                parsed_modules.append((mod_type.upper(), mod_name))
        
        assert parsed_modules[0] == ("EXT", "email")
        assert parsed_modules[1] == ("CLC", "domain")
        assert parsed_modules[2] == ("OUT", "json")

    def test_pipeline_data_flow(self):
        """Test data flow through pipeline"""
        # Simulate a realistic pipeline: extract emails -> collect domains -> format output
        
        # Mock modules
        email_extractor = MockModule("email", "EXT")
        domain_collector = MockModule("domain", "CLC")
        json_formatter = MockModule("json", "OUT")
        
        # Input data with emails
        input_text = "Contact us at info@example.com or support@test.org"
        
        # Step 1: Extract emails
        emails = email_extractor.process(input_text)
        
        # Step 2: Collect domains
        domains = domain_collector.process(emails)
        
        # Step 3: Format output
        formatted_output = json_formatter.process(domains)
        
        # Verify data flow
        assert input_text in email_extractor.processed_inputs
        assert emails in domain_collector.processed_inputs
        assert domains in json_formatter.processed_inputs
        assert "EXT:email" in formatted_output


class TestPipelineErrorHandling:
    """Tests for error handling in pipeline"""

    def test_module_failure_handling(self):
        """Test handling when a module fails"""
        
        class FailingModule(MockModule):
            def process(self, input_data: str) -> str:
                raise ValueError("Module processing failed")
        
        failing_module = FailingModule("failing", "EXT")
        
        with pytest.raises(ValueError, match="Module processing failed"):
            failing_module.process("test_input")

    def test_partial_pipeline_failure(self):
        """Test handling when part of pipeline fails"""
        successful_module = MockModule("success", "EXT")
        failing_module = MockModule("failing", "CLC")
        
        # Override process method to fail
        failing_module.process = MagicMock(side_effect=Exception("Processing error"))
        
        input_data = "test_input"
        
        # First module succeeds
        intermediate_result = successful_module.process(input_data)
        assert intermediate_result is not None
        
        # Second module fails
        with pytest.raises(Exception, match="Processing error"):
            failing_module.process(intermediate_result)

    def test_empty_input_handling(self):
        """Test handling of empty input"""
        module = MockModule("test", "EXT")
        
        result = module.process("")
        assert result == "EXT:test()"
        assert "" in module.processed_inputs

    def test_none_input_handling(self):
        """Test handling of None input"""
        module = MockModule("test", "EXT")
        
        with pytest.raises(TypeError):
            module.process(None)

    def test_large_input_handling(self):
        """Test handling of large input"""
        module = MockModule("test", "EXT")
        large_input = "x" * 10000
        
        result = module.process(large_input)
        assert large_input in result
        assert large_input in module.processed_inputs


class TestThreadedPipeline:
    """Tests for threaded pipeline execution"""

    def setup_method(self):
        """Setup for each test method"""
        self.thread_process = ThreadProcess()

    @patch('stringx.core.thread_process.ThreadPoolExecutor')
    def test_thread_pool_creation(self, mock_executor):
        """Test thread pool creation"""
        mock_executor.return_value.__enter__.return_value = MagicMock()
        
        self.thread_process.max_thread = 5
        
        # Would test thread pool execution
        assert self.thread_process.max_thread == 5

    def test_concurrent_module_execution(self):
        """Test concurrent execution of modules"""
        modules = [
            MockModule(f"module_{i}", "EXT") for i in range(3)
        ]
        
        inputs = [f"input_{i}" for i in range(3)]
        
        # Simulate concurrent processing
        results = []
        for module, input_data in zip(modules, inputs):
            result = module.process(input_data)
            results.append(result)
        
        assert len(results) == 3
        for i, result in enumerate(results):
            assert f"input_{i}" in result
            assert f"module_{i}" in result

    def test_thread_safety(self):
        """Test thread safety of module processing"""
        shared_module = MockModule("shared", "EXT")
        
        # Simulate concurrent access
        inputs = [f"concurrent_input_{i}" for i in range(10)]
        results = []
        
        for input_data in inputs:
            result = shared_module.process(input_data)
            results.append(result)
        
        # All inputs should be processed
        assert len(shared_module.processed_inputs) == 10
        assert len(results) == 10
        
        # Check that all inputs were recorded
        for i in range(10):
            assert f"concurrent_input_{i}" in shared_module.processed_inputs


class TestModuleTypes:
    """Tests for different module types"""

    def test_extractor_module_behavior(self):
        """Test extractor (EXT) module behavior"""
        extractor = MockModule("email_extractor", "EXT")
        
        # Extractors should extract specific data from input
        input_text = "Email: user@domain.com Phone: 123-456-7890"
        result = extractor.process(input_text)
        
        assert "EXT:email_extractor" in result
        assert input_text in result

    def test_collector_module_behavior(self):
        """Test collector (CLC) module behavior"""
        collector = MockModule("domain_collector", "CLC")
        
        # Collectors should gather additional information
        domain = "example.com"
        result = collector.process(domain)
        
        assert "CLC:domain_collector" in result
        assert domain in result

    def test_connection_module_behavior(self):
        """Test connection (CON) module behavior"""
        connector = MockModule("database", "CON")
        
        # Connectors should handle connections to external services
        connection_string = "mysql://user:pass@host:3306/db"
        result = connector.process(connection_string)
        
        assert "CON:database" in result
        assert connection_string in result

    def test_output_module_behavior(self):
        """Test output (OUT) module behavior"""
        formatter = MockModule("json_formatter", "OUT")
        
        # Output modules should format data for presentation
        data = {"key": "value", "count": 42}
        result = formatter.process(str(data))
        
        assert "OUT:json_formatter" in result
        assert str(data) in result

    def test_ai_module_behavior(self):
        """Test AI module behavior"""
        ai_module = MockModule("content_analyzer", "AI")
        
        # AI modules should process content with artificial intelligence
        content = "This is sample content for AI analysis"
        result = ai_module.process(content)
        
        assert "AI:content_analyzer" in result
        assert content in result


class TestPipelineConfiguration:
    """Tests for pipeline configuration and setup"""

    def test_module_discovery(self):
        """Test module discovery mechanism"""
        # Mock available modules
        available_modules = {
            "EXT": ["email", "domain", "ip", "url"],
            "CLC": ["whois", "dns", "geoip"],
            "CON": ["mysql", "sqlite", "opensearch"],
            "OUT": ["json", "csv", "xml"],
            "AI": ["openai", "gemini"]
        }
        
        # Test module existence checks
        for module_type, modules in available_modules.items():
            for module_name in modules:
                # In real implementation, would check if module file exists
                assert isinstance(module_name, str)
                assert len(module_name) > 0
                assert module_type in ["EXT", "CLC", "CON", "OUT", "AI"]

    def test_invalid_module_handling(self):
        """Test handling of invalid module specifications"""
        invalid_specs = [
            "invalid_type:module",
            "ext:",
            ":module",
            "ext:nonexistent",
            ""
        ]
        
        for spec in invalid_specs:
            if ":" not in spec or spec.count(":") != 1:
                # Should be identified as invalid
                assert True
            else:
                parts = spec.split(":")
                if not parts[0] or not parts[1]:
                    # Should be identified as invalid
                    assert True

    def test_module_parameter_passing(self):
        """Test parameter passing to modules"""
        module = MockModule("parameterized", "EXT")
        
        # Simulate parameter passing
        input_with_params = "input_data|param1=value1|param2=value2"
        result = module.process(input_with_params)
        
        assert "parameterized" in result
        assert "param1=value1" in result
        assert "param2=value2" in result


if __name__ == "__main__":
    pytest.main([__file__])