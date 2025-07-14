import subprocess
from datetime import datetime
import os

# ✅ Ambil token dan username dari environment (Replit Secrets)
GITHUB_ACTOR = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "Visinema/Database"
BRANCH = "main"

def git_push():
    try:
        if not GITHUB_ACTOR or not GITHUB_TOKEN:
            print("❌ Token atau Username GitHub tidak ditemukan di environment")
            return

        # 🔐 URL otentikasi dengan token
        auth_url = f"https://{GITHUB_ACTOR}:{GITHUB_TOKEN}@github.com/{REPO}.git"

        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "config", "user.name", "ReplitBot"], check=True)
        subprocess.run(["git", "config", "user.email", "bot@replit.com"], check=True)
        subprocess.run(["git", "remote", "remove", "origin"], check=False)
        subprocess.run(["git", "remote", "add", "origin", auth_url], check=True)

        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"🔄 Auto-update: {datetime.now().isoformat()}"], check=False)
        subprocess.run(["git", "pull", "--rebase", "origin", BRANCH], check=False)
        subprocess.run(["git", "push", "--force", "origin", BRANCH], check=True)

        print("✅ Push berhasil ke GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git command gagal: {e}")
    except Exception as e:
        print(f"❌ Error push ke GitHub: {e}")