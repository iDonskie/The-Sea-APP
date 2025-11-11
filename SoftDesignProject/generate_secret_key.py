#!/usr/bin/env python
"""
Generate a secure secret key for production deployment
"""
import secrets

print("=" * 60)
print("🔐 SECURE SECRET KEY GENERATOR")
print("=" * 60)
print("\nGenerated secret key for your production deployment:")
print("\n" + secrets.token_hex(32))
print("\n" + "=" * 60)
print("⚠️  IMPORTANT: Keep this key secret!")
print("Add it as an environment variable: SECRET_KEY")
print("=" * 60)
