from pathlib import Path

import pandas

import sklearn

import yaml

print("=" * 50)

print("RecoMart ML Data Platform")

print("=" * 50)

print("Python Packages")

print("✓ pandas")

print("✓ sklearn")

print("✓ yaml")

print()

folders = [

"config",

"data",

"src",

"docs",

"logs"

]

print("Checking folders")

for folder in folders:

    if Path(folder).exists():

        print(f"✓ {folder}")

    else:

        print(f"✗ {folder}")

print()

print("Environment Ready")
