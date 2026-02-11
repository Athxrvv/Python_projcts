# API Fuzzer – Security & Stability Testing Tool

A powerful automated API testing tool that sends high volumes of randomized and malformed inputs to REST endpoints to identify crashes, validation errors, and security weaknesses.

## Features

✅ **Automated Fuzzing**: Sends randomized and malformed payloads to API endpoints  
✅ **Security Testing**: Tests for SQL injection, XSS, command injection, and path traversal  
✅ **Edge Case Simulation**: Generates extreme values, type confusion, and format issues  
✅ **Dynamic Payloads**: Uses Faker library for realistic test data generation  
✅ **Structured Logging**: Detailed logging of all requests and responses  
✅ **Response Validation**: Analyzes API behavior under abnormal conditions  
✅ **Comprehensive Reports**: JSON reports with issue summaries and statistics  

## Tech Stack

- **Python 3.x**: Core programming language
- **Requests**: HTTP library for API calls
- **Faker**: Dynamic test payload generation
- **JSON**: Structured data handling

## Installation

```bash
cd api_fuzzer
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from fuzzer import APIFuzzer

# Initialize fuzzer with your API base URL
fuzzer = APIFuzzer(base_url="https://api.example.com")

# Fuzz a POST endpoint
fuzzer.fuzz_endpoint("/api/users", method="POST", num_requests=10)

# Generate report
report = fuzzer.generate_report()

# Save results
fuzzer.save_results("results.json")
```

### Running the Example

```bash
python fuzzer.py
```

This will fuzz the JSONPlaceholder test API and save results to `fuzzing_results.json`.

## Payload Types

The fuzzer automatically tests various attack vectors and edge cases:

### Security Tests
- **SQL Injection**: `' OR '1'='1`, `'; DROP TABLE users--`
- **XSS**: `<script>alert('XSS')</script>`, `<img src=x onerror=alert('XSS')>`
- **Command Injection**: `; ls -la`, `| cat /etc/passwd`
- **Path Traversal**: `../../etc/passwd`

### Edge Cases
- **Type Confusion**: Strings where numbers expected, arrays for single values
- **Extreme Values**: Negative numbers, very large integers, empty values
- **Long Strings**: 1000+ character inputs
- **Special Characters**: Unicode, symbols, control characters
- **Null/Undefined**: Null values, missing fields

### Realistic Data
- Uses Faker to generate:
  - Names, emails, addresses
  - Phone numbers, dates, URLs
  - Random text and descriptions

## Response Analysis

The fuzzer automatically detects:

- 🔴 **Server Errors** (5xx status codes)
- 🔴 **Information Disclosure** (stack traces, error messages)
- 🟡 **Slow Responses** (>5 seconds)
- 🟡 **Validation Bypasses** (suspicious payloads accepted)
- 🟡 **Large Responses** (potential DoS issues)
- 🔴 **Timeouts and Connection Errors**

## Report Structure

```json
{
  "summary": {
    "total_tests": 50,
    "errors": 5,
    "tests_with_issues": 12,
    "average_response_time": 0.234
  },
  "status_codes": {
    "200": 30,
    "400": 15,
    "500": 5
  },
  "issues_found": {
    "SERVER_ERROR": 5,
    "INFO_DISCLOSURE_EXCEPTION": 3,
    "SLOW_RESPONSE": 4
  },
  "critical_findings": [...]
}
```

## Advanced Usage

### Custom Payloads

```python
custom_payloads = [
    {"user_id": -1, "role": "admin"},
    {"token": "invalid_token_xyz"},
    {"data": "A" * 50000}
]

fuzzer.fuzz_endpoint(
    "/api/secure-endpoint",
    method="POST",
    custom_payloads=custom_payloads
)
```

### Testing Multiple Endpoints

```python
fuzzer = APIFuzzer(base_url="https://api.example.com")

endpoints = [
    ("/api/users", "POST"),
    ("/api/products", "PUT"),
    ("/api/orders", "DELETE")
]

for endpoint, method in endpoints:
    fuzzer.fuzz_endpoint(endpoint, method=method, num_requests=5)

fuzzer.save_results("complete_fuzzing_results.json")
```

### Timeout Configuration

```python
# Set custom timeout for slow APIs
fuzzer = APIFuzzer(base_url="https://slow-api.example.com", timeout=30)
```

## Best Practices

1. **Start Small**: Begin with a few requests to understand API behavior
2. **Rate Limiting**: Use delays between requests to avoid overwhelming the API
3. **Permission**: Only test APIs you have permission to test
4. **Staging Environment**: Test on staging/development environments first
5. **Review Results**: Manually verify critical findings before reporting
6. **Iterate**: Re-test after fixes are applied

## Logging

The fuzzer uses structured logging for all operations:

```
2024-01-01 12:00:00 - __main__ - INFO - Starting fuzzing on POST https://api.example.com/users
2024-01-01 12:00:00 - __main__ - WARNING - Test malformed_0: Found issues - SERVER_ERROR (Status: 500)
2024-01-01 12:00:01 - __main__ - ERROR - Server error 500
```

## Use Cases

✅ **Pre-Production Testing**: Identify issues before deployment  
✅ **Security Audits**: Find validation and injection vulnerabilities  
✅ **Regression Testing**: Ensure fixes don't break under edge cases  
✅ **Load Testing**: Stress test with high-volume requests  
✅ **API Hardening**: Proactively improve error handling  

## Limitations

- Does not test authentication flows automatically
- Requires valid network access to target API
- May trigger rate limiting on production APIs
- Results require manual interpretation for complex issues

## Contributing

Feel free to extend the fuzzer with:
- Additional payload types
- New analysis patterns
- Authentication support
- GraphQL support

## License

This tool is for educational and authorized testing purposes only. Always obtain permission before testing third-party APIs.

## Example Output

```
============================================================
FUZZING REPORT SUMMARY
============================================================
Total Tests: 45
Errors: 2
Tests with Issues: 8
Average Response Time: 0.156s
Status Codes: {200: 30, 400: 10, 500: 5}
Issues Found: {'SERVER_ERROR': 5, 'INFO_DISCLOSURE_EXCEPTION': 3}
============================================================
Fuzzing completed! Check fuzzing_results.json for details.
============================================================
```

## Support

For issues or questions, please open an issue in the repository.
