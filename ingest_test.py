"""Test ingestion with small limits - perfect for initial testing."""
import asyncio
import sys
from ingest.confluence_ingest import ingest_space
from ingest.jira_ingest import ingest_jql
from app.settings import settings


async def main():
    """Run test ingestion with small limits."""
    print("🧪 Starting TEST ingestion (small sample)...\n")
    print("This will ingest:")
    print("  - 5 Confluence pages (for testing)")
    print("  - 5 Jira issues (for testing)")
    print("")
    
    # Ingest Confluence - just 5 pages
    print("=" * 60)
    print("STEP 1: Ingesting 5 Confluence pages (test)")
    print("=" * 60)
    try:
        space_keys = [s.strip() for s in settings.conf_space_keys.split(",") if s.strip()]
        if space_keys:
            await ingest_space(space_keys[0], limit=5)
        else:
            print("No Confluence spaces configured")
    except Exception as e:
        print(f"❌ Error ingesting Confluence: {e}")
        sys.exit(1)
    
    # Ingest Jira - just 5 issues
    print("\n" + "=" * 60)
    print("STEP 2: Ingesting 5 Jira issues (test)")
    print("=" * 60)
    try:
        await ingest_jql(limit=5)
    except Exception as e:
        print(f"❌ Error ingesting Jira: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Test ingestion complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  - Test queries: uvicorn app.main:app --reload")
    print("  - If working well, run: python ingest_all.py (for full ingestion)")


if __name__ == "__main__":
    asyncio.run(main())


