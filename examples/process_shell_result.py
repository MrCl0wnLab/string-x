# This script processes the result from shell command
# {STRING} will be replaced with the shell command output

input_data = {STRING}

# Extract just the domain name from shell output like "Processing domain.com"
if 'Processing ' in input_data:
    domain = input_data.replace('Processing ', '')
else:
    domain = input_data

# Process with String-X functions
result = f"""
Shell Input: {input_data}
Extracted Domain: {domain}
MD5: {md5(domain)}
Base64: {base64(domain)}
Length: {len(domain)} characters
"""