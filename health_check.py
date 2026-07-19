from pathlib import Path
import importlib

print("=" * 50)
print("RecoMart ML Data Platform")
print("=" * 50)

packages = [
    "pandas",
    "yaml",
    "requests"
]

print("\nChecking Python packages")

for package in packages:
    try:
        importlib.import_module(package)
        print(f"✓ {package}")
    except ImportError:
        print(f"✗ {package}")

folders = [
    "config",
    "data",
    "src",
    "docs",
    "logs"
]

print("\nChecking project folders")

for folder in folders:
    if Path(folder).exists():
        print(f"✓ {folder}")
    else:
        print(f"✗ {folder}")

config = Path("config/config.yaml")

print("\nChecking configuration")

if config.exists():
    print("✓ config/config.yaml")
else:
    print("✗ config/config.yaml")

print("\nEnvironment Ready")