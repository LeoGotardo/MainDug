import hashlib

# Assume this is the hashed password stored in your database
stored_hashed_password = hashlib.sha256("123".encode()).hexdigest()

# This is the password attempt by a user
password_attempt = "123"

# Hash the password attempt
attempt_hashed = hashlib.sha256(password_attempt.encode()).hexdigest()

# Compare the hashes
if attempt_hashed == stored_hashed_password:
    print("Password matches!")
else:
    print("Password does not match.")

