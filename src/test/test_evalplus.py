import os
import subprocess
import pandas as pd
from pathlib import Patht
from subprocess import Popen, PIPE
import argparse
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.validator.arg_validator import validate_arguments
from src.util.constants import get_model_map, get_extension_map
from src.helper.model_path_helper import resolve_model_name_for_path
from src.test.test_utils import (
    setup_test_environment,
    compile_python_code,
    compile_java_code,
    initialize_python_process,
    initialize_java_process,
    run_and_validate_test_cases,
    get_test_input_and_output,
    cleanup_java_class_files,
    prepare_test_reports,
    cleanup_results_and_get_result_map
)

def main(args, is_algorithm_based_translation, dataset="evalplus"):
    test_env = setup_test_environment(args, dataset, is_algorithm_based_translation)

    translation_dir = test_env["translation_dir"]
    files = test_env["files"]
    result = test_env["result"]

    if args.source_lang == "python" and args.target_lang == "java":
        for file in files:
            try:
                print(f"Filename: {file}")
                compile_java_code(translation_dir, file)
            except subprocess.CalledProcessError as e:
                result.add_to_compile_failed_with_details(file, e.stderr.decode('utf-8'))
            except Exception as e:
                result.add_to_compile_failed_with_details(file, e)

        cleanup_java_class_files(translation_dir)
    else:
        print(f"Dataset: {dataset} does not support {args.source_lang} as source language and {args.target_lang} as target language")
        return

    move_compile_failed_translated_codes_for_evalplus(result.get_result_map(), translation_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="model used for code translation", required=True, type=str)
    parser.add_argument("--source_lang", help="source language of the translated code", required=True, type=str)
    parser.add_argument("--target_lang", help="target language of the translated code", required=True, type=str)
    parser.add_argument("--translation_type", help="type of translation to use", required=True, type=str)
    parser.add_argument("--report_dir", help="path to directory to store report", required=True, type=str)

    args = parser.parse_args()
    validate_arguments(args, is_test=True)

    is_algorithm_based_translation = args.translation_type == "algorithm"

    main(args, is_algorithm_based_translation)
