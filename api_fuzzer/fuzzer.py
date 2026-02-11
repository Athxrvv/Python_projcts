import requests
import json
import logging
from datetime import datetime
from faker import Faker
import random
import string
from typing import Dict, List, Optional, Any
import time

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class APIFuzzer:
    """
    API Fuzzer - Security & Stability Testing Tool
    
    Sends randomized and malformed inputs to REST endpoints to identify:
    - Crashes and unhandled exceptions
    - Validation errors
    - Security weaknesses
    - Response inconsistencies
    """
    
    def __init__(self, base_url: str, timeout: int = 10):
        """
        Initialize the API Fuzzer
        
        Args:
            base_url: Base URL of the API to test
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.faker = Faker()
        self.results = []
        
    def generate_random_string(self, length: int = 10) -> str:
        """Generate random string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def generate_malformed_payloads(self) -> List[Dict[str, Any]]:
        """
        Generate various malformed and edge case payloads
        
        Returns:
            List of test payloads
        """
        payloads = [
            # Empty payloads
            {},
            {"": ""},
            
            # SQL Injection attempts
            {"username": "admin' OR '1'='1", "password": "password"},
            {"id": "1 OR 1=1"},
            {"query": "'; DROP TABLE users--"},
            
            # XSS attempts
            {"name": "<script>alert('XSS')</script>"},
            {"comment": "<img src=x onerror=alert('XSS')>"},
            
            # Command injection
            {"file": "; ls -la"},
            {"path": "../../etc/passwd"},
            
            # Type confusion
            {"id": "not_a_number"},
            {"active": "true_string_not_bool"},
            {"count": [1, 2, 3]},
            
            # Extreme values
            {"age": -1},
            {"price": 999999999999999},
            {"quantity": 0},
            
            # Very long strings
            {"description": "A" * 10000},
            {"name": self.generate_random_string(1000)},
            
            # Special characters
            {"text": "!@#$%^&*(){}[]|\\:;\"'<>,.?/~`"},
            {"unicode": "☠️💀👻🔥"},
            
            # Null and undefined
            {"value": None},
            {"data": "null"},
            
            # Format issues
            {"email": "not-an-email"},
            {"url": "invalid://url"},
            {"date": "not-a-date"},
            
            # Faker-generated realistic but potentially problematic data
            {"name": self.faker.name()},
            {"email": self.faker.email()},
            {"address": self.faker.address()},
            {"phone": self.faker.phone_number()},
            {"text": self.faker.text(max_nb_chars=200)},
            
            # Array/nested confusion
            {"nested": {"deep": {"very": {"deep": "value"}}}},
            {"array": []},
            {"mixed": [1, "two", {"three": 3}, None]},
        ]
        
        return payloads
    
    def fuzz_endpoint(
        self, 
        endpoint: str, 
        method: str = "POST",
        num_requests: int = 10,
        custom_payloads: Optional[List[Dict]] = None
    ) -> List[Dict]:
        """
        Fuzz a specific API endpoint
        
        Args:
            endpoint: API endpoint path (e.g., '/api/users')
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            num_requests: Number of random requests to send
            custom_payloads: Optional custom payloads to test
            
        Returns:
            List of test results
        """
        url = f"{self.base_url}{endpoint}"
        results = []
        
        # Use custom payloads or generate malformed ones
        payloads = custom_payloads if custom_payloads else self.generate_malformed_payloads()
        
        logger.info(f"Starting fuzzing on {method} {url}")
        logger.info(f"Sending {len(payloads)} malformed payloads + {num_requests} random payloads")
        
        # Test with malformed payloads
        for idx, payload in enumerate(payloads):
            result = self._send_request(url, method, payload, f"malformed_{idx}")
            results.append(result)
            time.sleep(0.1)  # Small delay to avoid overwhelming the API
        
        # Test with random payloads
        for i in range(num_requests):
            random_payload = self._generate_random_payload()
            result = self._send_request(url, method, random_payload, f"random_{i}")
            results.append(result)
            time.sleep(0.1)
        
        self.results.extend(results)
        return results
    
    def _generate_random_payload(self) -> Dict[str, Any]:
        """Generate a random payload using Faker"""
        payload_types = [
            lambda: {"name": self.faker.name(), "email": self.faker.email()},
            lambda: {"id": random.randint(1, 1000), "active": random.choice([True, False])},
            lambda: {"text": self.faker.text(), "timestamp": str(datetime.now())},
            lambda: {"data": self.generate_random_string(random.randint(5, 50))},
            lambda: {self.generate_random_string(5): self.generate_random_string(10)},
        ]
        
        return random.choice(payload_types)()
    
    def _send_request(
        self, 
        url: str, 
        method: str, 
        payload: Dict, 
        test_id: str
    ) -> Dict:
        """
        Send a single request and analyze the response
        
        Args:
            url: Full URL to send request to
            method: HTTP method
            payload: Request payload
            test_id: Unique test identifier
            
        Returns:
            Dict containing test results
        """
        result = {
            "test_id": test_id,
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "method": method,
            "payload": payload,
            "status_code": None,
            "response_time": None,
            "error": None,
            "response_body": None,
            "issues_found": []
        }
        
        start_time = time.time()
        
        try:
            # Send request based on method
            if method.upper() == "GET":
                response = requests.get(url, params=payload, timeout=self.timeout)
            elif method.upper() == "POST":
                response = requests.post(url, json=payload, timeout=self.timeout)
            elif method.upper() == "PUT":
                response = requests.put(url, json=payload, timeout=self.timeout)
            elif method.upper() == "DELETE":
                response = requests.delete(url, json=payload, timeout=self.timeout)
            elif method.upper() == "PATCH":
                response = requests.patch(url, json=payload, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            result["status_code"] = response.status_code
            result["response_time"] = time.time() - start_time
            
            # Try to parse response body
            try:
                result["response_body"] = response.json()
            except:
                result["response_body"] = response.text[:500]  # Truncate long responses
            
            # Analyze response for issues
            self._analyze_response(response, result)
            
        except requests.exceptions.Timeout:
            result["error"] = "Request timeout"
            result["issues_found"].append("TIMEOUT")
            logger.warning(f"Test {test_id}: Request timeout")
            
        except requests.exceptions.ConnectionError:
            result["error"] = "Connection error"
            result["issues_found"].append("CONNECTION_ERROR")
            logger.warning(f"Test {test_id}: Connection error")
            
        except Exception as e:
            result["error"] = str(e)
            result["issues_found"].append("EXCEPTION")
            logger.error(f"Test {test_id}: Exception - {str(e)}")
        
        result["response_time"] = time.time() - start_time
        
        # Log interesting findings
        if result["issues_found"]:
            logger.warning(
                f"Test {test_id}: Found issues - {', '.join(result['issues_found'])} "
                f"(Status: {result['status_code']})"
            )
        
        return result
    
    def _analyze_response(self, response: requests.Response, result: Dict):
        """
        Analyze response for potential issues
        
        Args:
            response: Response object
            result: Result dictionary to update
        """
        # Check for server errors
        if 500 <= response.status_code < 600:
            result["issues_found"].append("SERVER_ERROR")
            logger.error(f"Server error {response.status_code}")
        
        # Check for slow response
        if result["response_time"] > 5:
            result["issues_found"].append("SLOW_RESPONSE")
        
        # Check for potential information disclosure
        response_lower = str(response.text).lower()
        disclosure_keywords = [
            "exception", "stack trace", "error at line",
            "sql", "database", "query failed",
            "path", "file not found"
        ]
        
        for keyword in disclosure_keywords:
            if keyword in response_lower:
                result["issues_found"].append(f"INFO_DISCLOSURE_{keyword.upper().replace(' ', '_')}")
                break
        
        # Check for unusual response lengths
        if len(response.text) > 100000:
            result["issues_found"].append("LARGE_RESPONSE")
        
        # Check for potential validation bypass (200 with suspicious payload)
        if response.status_code == 200:
            payload_str = str(result["payload"]).lower()
            if any(x in payload_str for x in ["<script>", "or 1=1", "drop table", "../"]):
                result["issues_found"].append("POTENTIAL_VALIDATION_BYPASS")
    
    def generate_report(self) -> Dict:
        """
        Generate a summary report of all fuzzing results
        
        Returns:
            Dictionary containing summary statistics and findings
        """
        if not self.results:
            return {"message": "No tests run yet"}
        
        total_tests = len(self.results)
        errors = sum(1 for r in self.results if r["error"])
        issues = sum(1 for r in self.results if r["issues_found"])
        
        status_codes = {}
        for r in self.results:
            code = r["status_code"]
            status_codes[code] = status_codes.get(code, 0) + 1
        
        all_issues = []
        for r in self.results:
            all_issues.extend(r["issues_found"])
        
        issue_summary = {}
        for issue in all_issues:
            issue_summary[issue] = issue_summary.get(issue, 0) + 1
        
        avg_response_time = sum(
            r["response_time"] for r in self.results if r["response_time"]
        ) / total_tests if total_tests > 0 else 0
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "errors": errors,
                "tests_with_issues": issues,
                "average_response_time": round(avg_response_time, 3)
            },
            "status_codes": status_codes,
            "issues_found": issue_summary,
            "critical_findings": [
                r for r in self.results 
                if any(keyword in str(r["issues_found"]) 
                       for keyword in ["SERVER_ERROR", "VALIDATION_BYPASS", "INFO_DISCLOSURE"])
            ]
        }
        
        logger.info("=" * 60)
        logger.info("FUZZING REPORT SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Errors: {errors}")
        logger.info(f"Tests with Issues: {issues}")
        logger.info(f"Average Response Time: {avg_response_time:.3f}s")
        logger.info(f"Status Codes: {status_codes}")
        logger.info(f"Issues Found: {issue_summary}")
        logger.info("=" * 60)
        
        return report
    
    def save_results(self, filename: str = "fuzzing_results.json"):
        """
        Save fuzzing results to a JSON file
        
        Args:
            filename: Output filename
        """
        with open(filename, 'w') as f:
            json.dump({
                "results": self.results,
                "report": self.generate_report()
            }, f, indent=2)
        
        logger.info(f"Results saved to {filename}")


def main():
    """Example usage of the API Fuzzer"""
    
    # Example: Fuzzing a mock API endpoint
    # Replace with your actual API URL
    fuzzer = APIFuzzer(base_url="https://jsonplaceholder.typicode.com")
    
    # Fuzz POST endpoint
    logger.info("Starting API Fuzzing Test...")
    fuzzer.fuzz_endpoint("/posts", method="POST", num_requests=5)
    
    # Generate and display report
    report = fuzzer.generate_report()
    
    # Save results
    fuzzer.save_results()
    
    print("\n" + "=" * 60)
    print("Fuzzing completed! Check fuzzing_results.json for details.")
    print("=" * 60)


if __name__ == "__main__":
    main()
