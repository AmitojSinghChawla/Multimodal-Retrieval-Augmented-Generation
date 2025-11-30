import os
import shutil
import atexit
from prettytable import PrettyTable
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT))

# ===== CONFIG =====
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", r"D:\Projects\Multimodal-Retrieval-Augmented-Generation\chroma_store")
DATA_DIR = os.getenv("DATA_DIR", r"D:\Projects\Multimodal-Retrieval-Augmented-Generation\uploaded_pdfs")

# ===== GLOBAL STATE =====
retriever = None


def initialize_retriever():
    """Initialize the vector database retriever once."""
    from VectorDB import initialize_vector_db

    global retriever
    if retriever is None:
        os.makedirs(VECTOR_DB_DIR, exist_ok=True)
        retriever = initialize_vector_db(VECTOR_DB_DIR)
        print(f"✅ Vector database initialized at: {VECTOR_DB_DIR}")
    return retriever


@atexit.register
def cleanup():
    """Delete vector database on exit."""
    if os.path.exists(VECTOR_DB_DIR):
        try:
            shutil.rmtree(VECTOR_DB_DIR)
            print(f"\n🗑️ Vector database deleted: {VECTOR_DB_DIR}")
        except Exception as e:
            print(f"⚠️ Could not delete vector database: {e}")


def display_menu():
    """Display the main menu using PrettyTable."""
    table = PrettyTable()
    table.field_names = ["Function", "Description", "Command"]
    table.add_row([
        "Ingest Files",
        "Process and add files to the vector database.",
        "1"
    ])
    table.add_divider()
    table.add_row([
        "Chat with Documents",
        "Ask questions and retrieve answers from ingested content.",
        "2"
    ])
    table.add_divider()
    table.add_row([
        "Exit",
        "End the session and delete vector database.",
        "3"
    ])

    print("\n" + "=" * 70)
    print("🤖 RAG Chatbot - Console Interface")
    print("=" * 70)
    print(table)


def run_ingestion():
    """Run ingestion from the configured data directory or user-provided path."""
    from Ingestion_chain import ingestion_chain

    print(f"\n📂 Default data directory: {DATA_DIR}")
    use_default = input("Use default directory? (y/n): ").strip().lower()

    if use_default == 'y':
        data_path = DATA_DIR
    else:
        data_path = input("Enter PDF file or directory path: ").strip()

    if not os.path.exists(data_path):
        print(f"❌ Path does not exist: {data_path}")
        return

    print(f"\n🚀 Running ingestion from: {data_path}")
    try:
        ret = initialize_retriever()
        ingestion_chain(data_path, ret)
        print("✅ Ingestion complete!")
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")


def run_chat():
    """Interactive chat loop with the RAG system."""
    from retrieval_chain import answer_question

    ret = initialize_retriever()

    print("\n" + "=" * 70)
    print("💬 Chat Mode Active")
    print("=" * 70)
    print("Commands:")
    print("  - Type your question to get answers")
    print("  - Type 'ingest' to add more files")
    print("  - Type 'end', 'break', or 'finish' to exit chat")
    print("=" * 70 + "\n")

    while True:
        query = input("You: ").strip()

        if not query:
            continue

        if query.lower() in ["end", "break", "finish", "exit", "quit"]:
            print("👋 Ending chat session.\n")
            break

        if query.lower() == "ingest":
            print("\n📁 Switching to ingestion mode...")
            run_ingestion()
            print("\n💬 Returning to chat mode...\n")
            continue

        try:
            response = answer_question(query, ret)
            print(f"\n🤖 Bot: {response}\n")
        except Exception as e:
            print(f"⚠️ Error: {e}\n")


def main():
    """Main application loop."""
    display_menu()

    try:
        while True:
            choice = input("\nEnter your command (1-3): ").strip()

            if choice == "1":
                run_ingestion()

            elif choice == "2":
                run_chat()

            elif choice == "3":
                print("\n🛑 Ending session...")
                break

            else:
                print("⚠️ Invalid command. Please enter 1, 2, or 3.")

    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user.")

    finally:
        print("👋 Goodbye!\n")


if __name__ == "__main__":
    main()