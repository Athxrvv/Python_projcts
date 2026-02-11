#!/usr/bin/env python3
"""
Example usage of the API Fuzzer tool

This script demonstrates various ways to use the fuzzer
for different testing scenarios.
"""

from fuzzer import APIFuzzer
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_basic_fuzzing():
    """Example 1: Basic fuzzing of a single endpoint"""
    logger.info("=" * 70)
    logger.info("EXAMPLE 1: Basic Fuzzing")
    logger.info("=" * 70)
    
    # Initialize fuzzer with JSONPlaceholder test API
    fuzzer = APIFuzzer(base_url="https://jsonplaceholder.typicode.com")
    
    # Fuzz the /posts endpoint with POST method
    fuzzer.fuzz_endpoint("/posts", method="POST", num_requests=5)
    
    # Generate and save report
    report = fuzzer.generate_report()
    fuzzer.save_results("example_basic_results.json")
    
    logger.info(f"Tests completed: {report['summary']['total_tests']}")
    logger.info(f"Issues found: {report['summary']['tests_with_issues']}")


def example_custom_payloads():
    """Example 2: Testing with custom payloads"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 2: Custom Payloads")
    logger.info("=" * 70)
    
    fuzzer = APIFuzzer(base_url="https://jsonplaceholder.typicode.com")
    
    # Define custom test payloads specific to your API
    custom_payloads = [
        # Test with very long title
        {
            "title": "A" * 1000,
            "body": "test",
            "userId": 1
        },
        # Test with negative user ID
        {
            "title": "Test",
            "body": "test",
            "userId": -1
        },
        # Test with missing required fields
        {
            "title": "Test"
        },
        # Test with wrong data types
        {
            "title": 12345,
            "body": ["array", "instead", "of", "string"],
            "userId": "not_a_number"
        },
    ]
    
    fuzzer.fuzz_endpoint(
        "/posts",
        method="POST",
        custom_payloads=custom_payloads,
        num_requests=2
    )
    
    report = fuzzer.generate_report()
    fuzzer.save_results("example_custom_results.json")
    
    logger.info(f"Custom payload tests: {len(custom_payloads)}")
    logger.info(f"Total tests: {report['summary']['total_tests']}")


def example_multiple_endpoints():
    """Example 3: Testing multiple endpoints"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 3: Multiple Endpoints")
    logger.info("=" * 70)
    
    fuzzer = APIFuzzer(base_url="https://jsonplaceholder.typicode.com")
    
    # Define endpoints to test
    endpoints = [
        ("/posts", "POST"),
        ("/posts/1", "PUT"),
        ("/comments", "POST"),
    ]
    
    # Fuzz each endpoint
    for endpoint, method in endpoints:
        logger.info(f"\nTesting {method} {endpoint}...")
        fuzzer.fuzz_endpoint(endpoint, method=method, num_requests=3)
    
    report = fuzzer.generate_report()
    fuzzer.save_results("example_multiple_results.json")
    
    logger.info(f"\nTotal endpoints tested: {len(endpoints)}")
    logger.info(f"Total tests executed: {report['summary']['total_tests']}")


def example_security_focused():
    """Example 4: Security-focused testing"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 4: Security-Focused Testing")
    logger.info("=" * 70)
    
    fuzzer = APIFuzzer(base_url="https://jsonplaceholder.typicode.com")
    
    # Define security-focused payloads
    security_payloads = [
        # SQL Injection attempts
        {"title": "admin' OR '1'='1", "body": "test", "userId": 1},
        {"title": "'; DROP TABLE posts--", "body": "test", "userId": 1},
        
        # XSS attempts
        {"title": "<script>alert('XSS')</script>", "body": "test", "userId": 1},
        {"title": "<img src=x onerror=alert('XSS')>", "body": "test", "userId": 1},
        
        # Command injection
        {"title": "; ls -la", "body": "test", "userId": 1},
        {"title": "| cat /etc/passwd", "body": "test", "userId": 1},
        
        # Path traversal
        {"title": "../../etc/passwd", "body": "test", "userId": 1},
        
        # NoSQL injection
        {"title": {"$gt": ""}, "body": "test", "userId": 1},
    ]
    
    fuzzer.fuzz_endpoint(
        "/posts",
        method="POST",
        custom_payloads=security_payloads,
        num_requests=0  # Only test our custom security payloads
    )
    
    report = fuzzer.generate_report()
    
    # Check for critical findings
    critical_count = len(report.get("critical_findings", []))
    logger.info(f"\nSecurity tests executed: {len(security_payloads)}")
    logger.info(f"Critical findings: {critical_count}")
    
    if critical_count > 0:
        logger.warning("⚠️  Critical security issues detected!")
        for finding in report["critical_findings"]:
            logger.warning(f"  - {finding['test_id']}: {finding['issues_found']}")
    
    fuzzer.save_results("example_security_results.json")


def example_performance_testing():
    """Example 5: Performance and load testing"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 5: Performance Testing")
    logger.info("=" * 70)
    
    fuzzer = APIFuzzer(base_url="https://jsonplaceholder.typicode.com", timeout=5)
    
    # Send a higher volume of requests
    logger.info("Sending high volume of requests...")
    fuzzer.fuzz_endpoint("/posts", method="POST", num_requests=20)
    
    report = fuzzer.generate_report()
    
    avg_time = report["summary"]["average_response_time"]
    logger.info(f"\nTotal requests: {report['summary']['total_tests']}")
    logger.info(f"Average response time: {avg_time:.3f}s")
    
    # Check for performance issues
    slow_responses = report["issues_found"].get("SLOW_RESPONSE", 0)
    if slow_responses > 0:
        logger.warning(f"⚠️  Found {slow_responses} slow responses (>5 seconds)")
    
    fuzzer.save_results("example_performance_results.json")


def main():
    """Run all examples"""
    logger.info("\n" + "=" * 70)
    logger.info("API FUZZER - EXAMPLE USAGE DEMONSTRATIONS")
    logger.info("=" * 70)
    
    try:
        # Run examples
        example_basic_fuzzing()
        example_custom_payloads()
        example_multiple_endpoints()
        example_security_focused()
        example_performance_testing()
        
        logger.info("\n" + "=" * 70)
        logger.info("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        logger.info("=" * 70)
        logger.info("\nCheck the following files for detailed results:")
        logger.info("  - example_basic_results.json")
        logger.info("  - example_custom_results.json")
        logger.info("  - example_multiple_results.json")
        logger.info("  - example_security_results.json")
        logger.info("  - example_performance_results.json")
        
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        raise


if __name__ == "__main__":
    main()
