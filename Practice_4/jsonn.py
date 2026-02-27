import json

# 1) Read JSON from file
with open("sample-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2) Print table header
print("Interface Status")
print("=" * 79)
print(f"{'DN':50} {'Description':18} {'Speed':7} {'MTU':4}")
print("-" * 79)

# 3) Go through items in "imdata"
for item in data.get("imdata", []):
    attrs = item["l1PhysIf"]["attributes"]

    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")

    # print as aligned columns
    print(f"{dn:50} {descr:18} {speed:7} {mtu:4}")