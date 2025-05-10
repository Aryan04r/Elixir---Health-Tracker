import secrets
SECRET_KEY = secrets.token_hex(32)  # This generates a 64-character random hex string
print(SECRET_KEY) 