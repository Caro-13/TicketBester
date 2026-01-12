"""
Test runner for TicketBester application.
Run all tests with: python run_tests.py
"""

import sys
import unittest
import os

# Add project root to path so 'src' package can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def run_all_tests():
    """Discover and run all tests in the tests directory"""

    print("=" * 70)
    print("🎫 TicketBester - Running Unit Tests")
    print("=" * 70)
    print()

    # Discover tests in src/tests directory
    loader = unittest.TestLoader()
    start_dir = 'src/tests'  # Changed from 'tests' to 'src/tests'
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print()
    print("=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"✅ Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print(f"⏭️  Skipped: {len(result.skipped)}")
    print("=" * 70)

    # Return exit code
    if result.wasSuccessful():
        print("\n🎉 All tests passed! 🎉\n")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the output above.\n")
        return 1


def run_specific_test(test_file):
    """Run a specific test file"""

    print("=" * 70)
    print(f"🎫 TicketBester - Running {test_file}")
    print("=" * 70)
    print()

    # Load specific test file
    loader = unittest.TestLoader()
    suite = loader.discover('src/tests', pattern=test_file)  # Changed

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


def print_usage():
    """Print usage instructions"""
    print("Usage:")
    print("  python run_tests.py              # Run all tests")
    print("  python run_tests.py db           # Run database tests only")
    print("  python run_tests.py launchers    # Run launcher tests only")
    print("  python run_tests.py --help       # Show this help")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg in ['--help', '-h', 'help']:
            print_usage()
            sys.exit(0)
        elif arg in ['db', 'database']:
            exit_code = run_specific_test('test_db_requests.py')
            sys.exit(exit_code)
        elif arg in ['launchers', 'main']:
            exit_code = run_specific_test('test_main_launchers.py')
            sys.exit(exit_code)
        else:
            print(f"Unknown argument: {arg}")
            print()
            print_usage()
            sys.exit(1)
    else:
        exit_code = run_all_tests()
        sys.exit(exit_code)