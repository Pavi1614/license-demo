# License Demo

License with signature, machine-id and expiry check.

## Run
python3 make_license.py
python3 verify.py

## Tests
- Tamper test - change max_hosts in LICENSE, verify shows INVALID
- Machine-ID test - copy LICENSE to another machine, verify shows NOT FOR THIS MACHINE
- Expiry test - change expiry to past date, verify shows EXPIRED
