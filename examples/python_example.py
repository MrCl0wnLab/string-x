# Example Python code for String-X execution
# This file demonstrates how to use Python code execution with String-X

# Access to the current string value via {STRING} placeholder
input_value = {STRING}

# Use String-X built-in functions
hash_md5 = md5(input_value)
hash_sha256 = sha256(input_value)
encoded_b64 = base64(input_value)

# Process the data
result = f"Input: {input_value}\nMD5: {hash_md5}\nSHA256: {hash_sha256}\nBase64: {encoded_b64}"

# The result variable will be returned as output