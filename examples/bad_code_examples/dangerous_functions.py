"""
⚠️ DANGEROUS FUNCTIONS EXAMPLE - FOR TESTING ONLY
"""

import os

def execute_user_command():
    command = input("Enter system command: ")
    
    # VIOLATION: os.system() allows command injection
    os.system(command)
    
    # VIOLATION: eval() executes arbitrary Python code
    user_expression = input("Enter math expression: ")
    result = eval(user_expression)
    
    return result

if __name__ == '__main__':
    print("Warning: This code is intentionally unsafe!")
