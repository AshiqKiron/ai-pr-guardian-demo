"""
⚠️ VULNERABLE CODE EXAMPLE - FOR TESTING ONLY
This file intentionally contains security violations to test AI-PR Guardian
"""

import os
import pickle

# VIOLATION 1: Hardcoded API Key (CRITICAL)
api_key = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyz"
secret_token = "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij"

# VIOLATION 2: AWS Credentials (CRITICAL)
aws_access_key = "AKIAIOSFODNN7EXAMPLE"

# VIOLATION 3: Database Password (CRITICAL)
db_password = "SuperSecretPassword123!"

def process_user_input():
    """Process user input - CONTAINS MULTIPLE VIOLATIONS"""
    
    # VIOLATION 4: Using eval() (HIGH)
    user_code = input("Enter Python code to execute: ")
    result = eval(user_code)  # DANGEROUS!
    
    # VIOLATION 5: Using exec() (HIGH)
    command = "import os; os.system('ls -la')"
    exec(command)  # DANGEROUS!
    
    # VIOLATION 6: os.system() (HIGH)
    os.system("rm -rf /tmp/*")  # Should use subprocess instead
    
    return result

if __name__ == '__main__':
    print("This is a vulnerable test file!")
    process_user_input()
