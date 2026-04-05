#!/usr/bin/env python3
"""
PhishGuard Web Dashboard Launcher
Run this script to start the PhishGuard email security analysis dashboard.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main launcher function"""
    print("🛡️ PhishGuard Email Security Analysis Engine")
    print("=" * 50)

    # Check if we're in the right directory
    web_dir = Path(__file__).parent / "phishguard_web"
    if not web_dir.exists():
        print("❌ Error: phishguard_web directory not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)

    # Change to web directory
    os.chdir(web_dir)

    print("📁 Working directory:", os.getcwd())
    print("🌐 Starting Flask web server...")

    try:
        # Start Flask app
        cmd = [sys.executable, "app.py"]
        print(f"🚀 Executing: {' '.join(cmd)}")
        print("\n" + "=" * 50)
        print("📋 Dashboard will be available at:")
        print("   http://localhost:5000")
        print("=" * 50)
        print("📖 Navigation:")
        print("   • Dashboard: Overview and statistics")
        print("   • Analyze: Upload and analyze email files")
        print("   • History: View past analyses")
        print("   • Statistics: Charts and trends")
        print("   • Settings: Configure parameters")
        print("   • Compliance: Audit reports")
        print("=" * 50)
        print("🛑 Press Ctrl+C to stop the server")
        print()

        subprocess.run(cmd)

    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()