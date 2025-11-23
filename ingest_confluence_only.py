"""Ingest only Confluence pages (with optional limit)."""
import asyncio
import sys
import argparse
from ingest.confluence_ingest import ingest_space, ingest_all_spaces
from app.settings import settings


async def main():
    """Run Confluence ingestion only."""
    parser = argparse.ArgumentParser(description="Ingest Confluence pages")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of pages to ingest (for testing). Example: --limit 10"
    )
    parser.add_argument(
        "--space",
        type=str,
        default=None,
        help="Specific space key to ingest (default: all configured spaces)"
    )
    
    args = parser.parse_args()
    
    if args.limit:
        print(f"🧪 Ingesting {args.limit} Confluence pages (test mode)...\n")
    else:
        print("📥 Ingesting all Confluence pages...\n")
    
    try:
        if args.space:
            # Ingest specific space
            await ingest_space(args.space, limit=args.limit)
        else:
            # Ingest all configured spaces
            space_keys = [s.strip() for s in settings.conf_space_keys.split(",") if s.strip()]
            if not space_keys:
                print("❌ No Confluence spaces configured")
                sys.exit(1)
            
            for space_key in space_keys:
                await ingest_space(space_key, limit=args.limit)
        
        print("\n✅ Confluence ingestion complete!")
        
    except Exception as e:
        print(f"❌ Error ingesting Confluence: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


