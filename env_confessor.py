#!/usr/bin/env python3
# Environment Variable Confessional - Where your secrets come to confess their sins

import os
import sys
import re
from pathlib import Path

def find_env_files():
    """Find all the .env files hiding in shame"""
    env_patterns = ['.env*', 'config/*', 'settings/*', '*.config']
    found_files = []
    
    for pattern in env_patterns:
        for path in Path('.').glob(pattern):
            if path.is_file():
                found_files.append(str(path))
    
    # Also check for the classic "I'll just hardcode it" files
    suspect_files = ['docker-compose.yml', 'docker-compose.yaml', 'app.py', 'main.py', 'config.py']
    for suspect in suspect_files:
        if Path(suspect).exists():
            found_files.append(suspect)
    
    return sorted(set(found_files))

def confess_secrets(filepath):
    """Make the environment variables confess their origins"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        return f"  [ERROR READING FILE: {e}]"
    
    # Look for environment variable patterns
    env_patterns = [
        r'\b[A-Z_][A-Z0-9_]*\s*=',  # .env files
        r'\${([A-Z_][A-Z0-9_]*)}',   # ${VAR} format
        r'\$([A-Z_][A-Z0-9_]*)',     # $VAR format
        r'process\.env\.([A-Z_][A-Z0-9_]*)',  # Node.js style
        r'os\.getenv\(\s*["\']([A-Z_][A-Z0-9_]*)["\']',  # Python
    ]
    
    confessions = []
    for pattern in env_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            var_name = match if isinstance(match, str) else match[0] if match else match
            if var_name:
                # Check if this variable is actually set in the environment
                actual_value = os.getenv(var_name)
                status = "✓ SET" if actual_value else "✗ MISSING"
                
                # Don't repeat confessions
                if var_name not in [c[0] for c in confessions]:
                    confessions.append((var_name, status))
    
    return confessions

def main():
    """Main confession booth"""
    print("\n=== ENVIRONMENT VARIABLE CONFESSIONAL ===")
    print("Where your secrets come clean about their messy lives\n")
    
    env_files = find_env_files()
    
    if not env_files:
        print("No sinners found! (No .env files detected)")
        return
    
    all_sins = {}
    
    for filepath in env_files:
        print(f"\n📁 {filepath}:")
        confessions = confess_secrets(filepath)
        
        if isinstance(confessions, str):
            print(confessions)
        elif confessions:
            for var_name, status in confessions:
                print(f"  {var_name}: {status}")
                all_sins[var_name] = all_sins.get(var_name, []) + [filepath]
        else:
            print("  (No environment variables found - suspiciously clean!)")
    
    # Summary of the worst offenders
    print("\n=== WORST OFFENDERS (Most Promiscuous Variables) ===")
    for var_name, locations in sorted(all_sins.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
        if len(locations) > 1:
            print(f"{var_name}: Found in {len(locations)} places ({', '.join(locations[:3])})")
    
    print("\nConfession complete. Go forth and refactor!")

if __name__ == "__main__":
    main()
