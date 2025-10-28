import subprocess
import platform

def ensure_ollama_running():
    try:
        # Check if Ollama is running
        result = subprocess.run(
            ["ollama", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            print("✅ Ollama is running.")
            return
    except FileNotFoundError:
        print("❌ Ollama not found in PATH.")
        return

    # If it reaches here, Ollama isn't running
    print("⚠️ Ollama not running. Starting it now...")

    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.Popen(["open", "-a", "Ollama"])
    elif system == "Windows":
        subprocess.Popen(
            ["cmd", "/c", "start", "ollama"],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    elif system == "Linux":
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        print(f"Unsupported OS: {system}")
        return

    print("🚀 Ollama started successfully.")

# Usage
if __name__ == "__main__":
    ensure_ollama_running()
