# Advanced Python example for String-X
# Demonstrates various String-X functions and Python capabilities

# Get the input value
domain = {STRING}

# Use String-X hash functions
md5_hash = md5(domain)
sha256_hash = sha256(domain)

# Use String-X encoding functions
base64_encoded = base64(domain)
hex_encoded = hex(domain)

# Use String-X network functions
try:
    domain_ip = ip(domain) if '.' in domain else 'N/A'
except:
    domain_ip = 'N/A'

# Use String-X validation functions
email_valid = email_validator(domain) if '@' in domain else 'N/A'

# Generate some random values
random_string = str_rand('8')
random_number = int_rand('6')

# Process and format results
analysis = {
    'domain': domain,
    'length': len(domain),
    'md5': md5_hash,
    'sha256': sha256_hash,
    'base64': base64_encoded,
    'hex': hex_encoded,
    'ip': domain_ip,
    'email_valid': email_valid,
    'random_str': random_string,
    'random_num': random_number,
    'timestamp': 'processed'
}

# Format the output
result = f"""
Domain Analysis: {domain}
===================
Length: {analysis['length']} characters
MD5: {analysis['md5']}
SHA256: {analysis['sha256']}
Base64: {analysis['base64']}
Hex: {analysis['hex']}
IP: {analysis['ip']}
Email Valid: {analysis['email_valid']}
Random String: {analysis['random_str']}
Random Number: {analysis['random_num']}
Status: {analysis['timestamp']}
"""