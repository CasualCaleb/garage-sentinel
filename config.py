import os
from dotenv import load_dotenv

load_dotenv()

SESSION_SECRET=os.getenv("SESSION_SECRET")

# GOOGLE
GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET")

# DISCORD
DISCORD_CLIENT_ID=os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET=os.getenv("DISCORD_CLIENT_SECRET")

# GITHUB
GITHUB_CLIENT_ID=os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET=os.getenv("GITHUB_CLIENT_SECRET")

if SESSION_SECRET is None:
    raise RuntimeError("SESSION_SECRET not set")

if GOOGLE_CLIENT_ID is None:
    raise RuntimeError("GOOGLE_CLIENT_ID not set")
if GOOGLE_CLIENT_SECRET is None:
    raise RuntimeError("GOOGLE_CLIENT_SECRET not set")

if DISCORD_CLIENT_ID is None:
    raise RuntimeError("DISCORD_CLIENT_ID not set")
if DISCORD_CLIENT_SECRET is None:
    raise RuntimeError("DISCORD_CLIENT_SECRET not set")

if GITHUB_CLIENT_ID is None:
    raise RuntimeError("GITHUB_CLIENT_ID not set")
if GITHUB_CLIENT_SECRET is None:
    raise RuntimeError("GITHUB_CLIENT_SECRET not set")