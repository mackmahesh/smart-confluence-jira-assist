"""Ingest only Jira issues (with optional limit)."""
import asyncio
import sys
import argparse
from ingest.jira_ingest import ingest_jql


async def main():
    """Run Jira ingestion only."""
    parser = argparse.ArgumentParser(description="Ingest Jira issues")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of issues to ingest (for testing). Example: --limit 10"
    )
    
    args = parser.parse_args()
    
    if args.limit:
        print(f"🧪 Ingesting {args.limit} Jira issues (test mode)...\n")
    else:
        print("📥 Ingesting all Jira issues...\n")
    
    try:
        await ingest_jql(limit=args.limit)
        print("\n✅ Jira ingestion complete!")
        
    except Exception as e:
        print(f"❌ Error ingesting Jira: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

