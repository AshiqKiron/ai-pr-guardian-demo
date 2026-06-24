# VIOLATION 1: Hardcoded Secret
api_key = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyz"

# VIOLATION 2: Dangerous Function
def run_code():
    user_input = input("Enter code: ")
    eval(user_input) 
