import pytest
import json
from fuzzer import APIFuzzer
from unittest.mock import Mock, patch
import requests


class TestAPIFuzzer:
    """Test suite for API Fuzzer"""
    
    def test_initialization(self):
        """Test fuzzer initialization"""
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        assert fuzzer.base_url == "https://api.example.com"
        assert fuzzer.timeout == 10
        assert fuzzer.results == []
    
    def test_base_url_trailing_slash(self):
        """Test that trailing slash is removed from base URL"""
        fuzzer = APIFuzzer(base_url="https://api.example.com/")
        assert fuzzer.base_url == "https://api.example.com"
    
    def test_generate_random_string(self):
        """Test random string generation"""
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        random_str = fuzzer.generate_random_string(10)
        assert len(random_str) == 10
        assert random_str.isalnum()
    
    def test_generate_malformed_payloads(self):
        """Test malformed payload generation"""
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        payloads = fuzzer.generate_malformed_payloads()
        
        # Check that we have multiple payloads
        assert len(payloads) > 20
        
        # Check for various payload types
        payload_strs = [str(p) for p in payloads]
        combined = ' '.join(payload_strs)
        
        # Security tests
        assert "OR '1'='1" in combined  # SQL injection
        assert "<script>" in combined  # XSS
        assert "DROP TABLE" in combined  # SQL injection
        
        # Edge cases
        assert {} in payloads  # Empty payload
        assert any(p.get("age") == -1 for p in payloads)  # Negative number
    
    def test_generate_random_payload(self):
        """Test random payload generation"""
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        payload = fuzzer._generate_random_payload()
        assert isinstance(payload, dict)
        assert len(payload) > 0
    
    @patch('requests.post')
    def test_send_request_success(self, mock_post):
        """Test successful request sending"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_response.text = '{"success": true}'
        mock_post.return_value = mock_response
        
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        result = fuzzer._send_request(
            "https://api.example.com/test",
            "POST",
            {"test": "data"},
            "test_1"
        )
        
        assert result["test_id"] == "test_1"
        assert result["status_code"] == 200
        assert result["error"] is None
        assert result["response_body"] == {"success": True}
    
    @patch('requests.post')
    def test_send_request_server_error(self, mock_post):
        """Test request with server error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.side_effect = json.JSONDecodeError("No JSON", "", 0)
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        result = fuzzer._send_request(
            "https://api.example.com/test",
            "POST",
            {"test": "data"},
            "test_2"
        )
        
        assert result["status_code"] == 500
        assert "SERVER_ERROR" in result["issues_found"]
    
    @patch('requests.post')
    def test_send_request_timeout(self, mock_post):
        """Test request timeout handling"""
        mock_post.side_effect = requests.exceptions.Timeout()
        
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        result = fuzzer._send_request(
            "https://api.example.com/test",
            "POST",
            {"test": "data"},
            "test_3"
        )
        
        assert result["error"] == "Request timeout"
        assert "TIMEOUT" in result["issues_found"]
    
    @patch('requests.post')
    def test_send_request_connection_error(self, mock_post):
        """Test connection error handling"""
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        result = fuzzer._send_request(
            "https://api.example.com/test",
            "POST",
            {"test": "data"},
            "test_4"
        )
        
        assert result["error"] == "Connection error"
        assert "CONNECTION_ERROR" in result["issues_found"]
    
    @patch('requests.post')
    def test_analyze_response_info_disclosure(self, mock_post):
        """Test information disclosure detection"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Exception at line 42: Stack trace follows..."
        mock_response.json.side_effect = json.JSONDecodeError("No JSON", "", 0)
        mock_post.return_value = mock_response
        
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        result = fuzzer._send_request(
            "https://api.example.com/test",
            "POST",
            {"test": "data"},
            "test_5"
        )
        
        # Check that info disclosure was detected
        assert any("INFO_DISCLOSURE" in issue for issue in result["issues_found"])
    
    @patch('requests.post')
    def test_analyze_response_validation_bypass(self, mock_post):
        """Test potential validation bypass detection"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"status": "ok"}'
        mock_response.json.return_value = {"status": "ok"}
        mock_post.return_value = mock_response
        
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        result = fuzzer._send_request(
            "https://api.example.com/test",
            "POST",
            {"query": "' OR 1=1--"},
            "test_6"
        )
        
        # Suspicious payload accepted with 200
        assert "POTENTIAL_VALIDATION_BYPASS" in result["issues_found"]
    
    @patch('requests.get')
    def test_http_methods(self, mock_get):
        """Test different HTTP methods"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_get.return_value = mock_response
        
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        result = fuzzer._send_request(
            "https://api.example.com/test",
            "GET",
            {"param": "value"},
            "test_7"
        )
        
        assert result["status_code"] == 200
        mock_get.assert_called_once()
    
    @patch('requests.post')
    def test_fuzz_endpoint(self, mock_post):
        """Test fuzzing an endpoint"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}
        mock_response.text = '{"status": "ok"}'
        mock_post.return_value = mock_response
        
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        results = fuzzer.fuzz_endpoint("/test", method="POST", num_requests=2)
        
        # Should have malformed payloads + 2 random requests
        assert len(results) > 2
        assert all(isinstance(r, dict) for r in results)
    
    @patch('requests.post')
    def test_generate_report(self, mock_post):
        """Test report generation"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_post.return_value = mock_response
        
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        fuzzer.fuzz_endpoint("/test", method="POST", num_requests=2)
        
        report = fuzzer.generate_report()
        
        assert "summary" in report
        assert "total_tests" in report["summary"]
        assert "status_codes" in report
        assert report["summary"]["total_tests"] > 0
    
    @patch('requests.post')
    def test_save_results(self, mock_post, tmp_path):
        """Test saving results to file"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_post.return_value = mock_response
        
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        fuzzer.fuzz_endpoint("/test", method="POST", num_requests=1)
        
        output_file = tmp_path / "test_results.json"
        fuzzer.save_results(str(output_file))
        
        assert output_file.exists()
        
        # Verify file content
        with open(output_file) as f:
            data = json.load(f)
            assert "results" in data
            assert "report" in data
    
    def test_empty_report(self):
        """Test report generation with no results"""
        fuzzer = APIFuzzer(base_url="https://api.example.com")
        report = fuzzer.generate_report()
        assert "message" in report
        assert report["message"] == "No tests run yet"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
