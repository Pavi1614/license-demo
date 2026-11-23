import json, os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

# 1. Use old keys if they exist, else make new ones
if os.path.exists("private.key"):
    with open("private.key", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
else:
    private_key = Ed25519PrivateKey.generate()
    with open("private.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

public_key = private_key.public_key()
with open("public.key", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

# 2. Get machine_id
with open("/etc/machine-id") as f:
    machine_id = f.read().strip()

# 3. Make LICENSE with machine_id
license_data = {
    "tenant": "test-tenant",
    "plan": "standard",
    "max_hosts": 10,
    "expiry": "2027-01-01",
    "machine_id": machine_id
}

data = json.dumps(license_data, indent=2).encode()
with open("LICENSE", "wb") as f:
    f.write(data)

# 4. Sign LICENSE
signature = private_key.sign(data)
with open("license.sig", "wb") as f:
    f.write(signature)

print("Done. Keys and signature created.")
print("machine_id:", machine_id)
