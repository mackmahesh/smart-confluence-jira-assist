"""Script to run all ingestion tasks."""
import asyncio
import sys
from ingest.confluence_ingest import ingest_all_spaces
from ingest.jira_ingest import ingest_jql


async def main():
    """Run all ingestion tasks."""
    print("🚀 Starting full ingestion process...\n")
    
    # Ingest Confluence
    print("=" * 60)
    print("STEP 1: Ingesting Confluence spaces")
    print("=" * 60)
    try:
        await ingest_all_spaces()
    except Exception as e:
        print(f"❌ Error ingesting Confluence: {e}")
        sys.exit(1)
    
    # Ingest Jira
    print("\n" + "=" * 60)
    print("STEP 2: Ingesting Jira issues")
    print("=" * 60)
    try:
        await ingest_jql()
    except Exception as e:
        print(f"❌ Error ingesting Jira: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Ingestion complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

