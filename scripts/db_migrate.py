#!/usr/bin/env python3
"""
Database migration helper script.

Helps migrate from SQLite to PostgreSQL for production.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.db import engine, Base
from app.models import (
    Article, Keyword, RepurposedContent, UserConsent,
    TrackingEvent, AuditLog
)


def create_tables():
    """Create all tables in the database."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")


def drop_tables():
    """Drop all tables (use with caution!)."""
    confirm = input("⚠️  This will DROP all tables. Type 'yes' to confirm: ")
    if confirm.lower() != 'yes':
        print("Cancelled")
        return
    
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables dropped")


def check_connection():
    """Test database connection."""
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print(f"✅ Database connection successful")
            print(f"   Database URL: {settings.DATABASE_URL}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def show_tables():
    """Show all tables in database."""
    from sqlalchemy import inspect
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if tables:
        print(f"📊 Tables in database ({len(tables)}):")
        for table in tables:
            print(f"   - {table}")
    else:
        print("No tables found in database")


def migrate_sqlite_to_postgres():
    """
    Migrate data from SQLite to PostgreSQL.
    
    This is a helper function - customize as needed.
    """
    print("⚠️  Migration helper - customize for your needs")
    print()
    print("Steps:")
    print("1. Export data from SQLite:")
    print("   sqlite3 autocash.db .dump > backup.sql")
    print()
    print("2. Convert to PostgreSQL format:")
    print("   # Remove SQLite-specific syntax")
    print("   # Adjust data types")
    print()
    print("3. Import to PostgreSQL:")
    print("   psql -U autocash_user -d autocash_db < backup.sql")
    print()
    print("Or use a tool like pgloader:")
    print("   pgloader autocash.db postgresql://user:pass@localhost/autocash_db")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database migration helper")
    parser.add_argument(
        'action',
        choices=['create', 'drop', 'check', 'show', 'migrate-help'],
        help='Action to perform'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("autocash-ultimate Database Migration Helper")
    print("=" * 60)
    print()
    
    if args.action == 'create':
        create_tables()
    elif args.action == 'drop':
        drop_tables()
    elif args.action == 'check':
        check_connection()
    elif args.action == 'show':
        show_tables()
    elif args.action == 'migrate-help':
        migrate_sqlite_to_postgres()
    
    print()


if __name__ == "__main__":
    main()
