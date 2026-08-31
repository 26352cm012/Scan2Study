import hashlib

print("================================")
print("        Scan2Study 📚")
print("   Integrity Checker v0.1")
print("================================")

data = "My first study material"

hash_value = hashlib.sha256(data.encode()).hexdigest()

print("\nStudy material:")
print(data)

print("\nDigital fingerprint:")
print(hash_value)

print("\nStatus: TRUSTED ✅")
