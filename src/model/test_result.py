class TestResult:
    def __init__(self):
        self.test_passed = set()
        self.compile_failed = set()
        self.runtime_failed = set()
        self.test_failed = set()
        self.infinite_loop = set()
        self.test_failed_details = {}
        self.compile_failed_details = {}
        self.runtime_failed_details = {}

    def add_to_test_passed(self, file):
        self.test_passed.add(file)

    def add_to_compile_failed_with_details(self, file, error):
        self.compile_failed.add(file)

        if file not in self.compile_failed_details:
            self.compile_failed_details[file] = set()

        self.compile_failed_details[file].add(f"Error: {str(error)}")

    def add_to_runtime_failed_with_details(self, file, error, test_index=None):
        self.runtime_failed.add(file)
        
        if file not in self.runtime_failed_details:
            self.runtime_failed_details[file] = set()
        
        self.runtime_failed_details[file].add(f"{'Test Index: ' + str(test_index) + ' ' if test_index is not None else ''}Error: {str(error)}")

    def add_to_test_failed_with_details(self, file, expected, output, test_index=None):
        self.test_failed.add(file)
        
        if file not in self.test_failed_details:
            self.test_failed_details[file] = set()
        
        self.test_failed_details[file].add(f"{'Test Index: ' + str(test_index) + ' ' if test_index is not None else ''}Actual: {str(expected)} Generated: {str(output)}")

    def add_to_infinite_loop(self, file):
        self.infinite_loop.add(file)

    def cleanup_results(self):
        self.infinite_loop -= self.test_failed

    def get_result_map(self):
        return {
            "test_passed": list(self.test_passed),
            "compile_failed": list(self.compile_failed),
            "runtime_failed": list(self.runtime_failed),
            "test_failed": list(self.test_failed),
            "infinite_loop": list(self.infinite_loop),
            "test_failed_details": {file_name: list(details) for file_name, details in self.test_failed_details.items()},
            "compile_failed_details": {file_name: list(details) for file_name, details in self.compile_failed_details.items()},
            "runtime_failed_details": {file_name: list(details) for file_name, details in self.runtime_failed_details.items()}
        }
