import json
from datetime import date
from cryptography.hazmat.primitives import serialization

# 1. Read LICENSE as JSON
with open("LICENSE", "rb") as f:
    data = f.read()

license_data = json.loads(data)

# 2. Check expiry
today = str(date.today())
if today > license_data["expiry"]:
    print("EXPIRED")
    exit()

# 3. Check machine_id - only if it exists in LICENSE
if "machine_id" in license_data:
    with open("/etc/machine-id") as f:
        current_id = f.read().strip()
    if current_id != license_data["machine_id"]:
        print("INVALID - NOT FOR THIS MACHINE")
        exit()
else:
    print("Note: no machine_id in LICENSE, skipping machine check")

# 4. Check signature
with open("license.sig", "rb") as f:
    signature = f.read()

with open("public.key", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

try:
    public_key.verify(signature, data)
    print("VALID - License is real, not changed")
except:
    print("INVALID - License is fake or tampered")
