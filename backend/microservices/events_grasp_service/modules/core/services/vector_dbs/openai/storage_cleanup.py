#!/usr/bin/env python3
"""
OpenAI Storage Cleanup Script

Deletes files and vector stores from OpenAI storage.
Provides options to:
- Delete all files
- Delete all vector stores
- Delete only files/stores matching specific names
- Dry-run mode to preview what would be deleted
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Optional

from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OpenAIStorageManager:
    """Manager for cleaning up OpenAI storage (files and vector stores)."""

    def __init__(self):
        """Initialize the storage manager."""
        self.client = self._init_client()

    def _init_client(self) -> OpenAI:
        """Initialize OpenAI client."""
        api_key = os.environ.get('OPENAI_API_KEY')

        if not api_key:
            # Try to load from file
            key_file = Path.home() / "runtime_data" / "keys" / "openai" / "openai_api_key.txt"
            if key_file.exists():
                api_key = key_file.read_text().strip()
                os.environ['OPENAI_API_KEY'] = api_key
            else:
                raise ValueError(
                    "OPENAI_API_KEY not found. Please run 'npm run setup:openai' first."
                )

        return OpenAI(api_key=api_key)

    def list_all_files(self) -> List[Dict]:
        """List all files in OpenAI storage."""
        files = self.client.files.list()
        return [
            {
                'id': f.id,
                'filename': f.filename,
                'purpose': f.purpose,
                'bytes': f.bytes,
                'created_at': f.created_at
            }
            for f in files.data
        ]

    def list_all_vector_stores(self) -> List[Dict]:
        """List all vector stores in OpenAI."""
        stores = self.client.vector_stores.list()
        return [
            {
                'id': s.id,
                'name': s.name,
                'file_counts': {
                    'total': s.file_counts.total,
                    'completed': s.file_counts.completed,
                    'in_progress': s.file_counts.in_progress,
                    'failed': s.file_counts.failed
                },
                'created_at': s.created_at
            }
            for s in stores.data
        ]

    def delete_file(self, file_id: str) -> bool:
        """Delete a single file."""
        try:
            self.client.files.delete(file_id)
            return True
        except Exception as e:
            logger.warning(f"Could not delete file {file_id}: {e}")
            return False

    def delete_vector_store(self, store_id: str, delete_files: bool = True) -> Dict:
        """
        Delete a vector store and optionally its files.

        Args:
            store_id: Vector store ID
            delete_files: If True, also delete files attached to the store

        Returns:
            Dictionary with deletion results
        """
        deleted_files = []

        # Delete files first if requested
        if delete_files:
            try:
                vs_files = self.client.vector_stores.files.list(vector_store_id=store_id)
                for vs_file in vs_files.data:
                    if self.delete_file(vs_file.id):
                        deleted_files.append(vs_file.id)
            except Exception as e:
                logger.warning(f"Could not list files for store {store_id}: {e}")

        # Delete the vector store
        try:
            self.client.vector_stores.delete(store_id)
            return {'success': True, 'files_deleted': deleted_files}
        except Exception as e:
            logger.error(f"Could not delete vector store {store_id}: {e}")
            return {'success': False, 'error': str(e), 'files_deleted': deleted_files}

    def delete_all_files(self, dry_run: bool = False, filter_purpose: Optional[str] = None) -> Dict:
        """
        Delete all files from OpenAI storage.

        Args:
            dry_run: If True, only show what would be deleted
            filter_purpose: Only delete files with this purpose (e.g., 'assistants')

        Returns:
            Dictionary with deletion results
        """
        files = self.list_all_files()

        if filter_purpose:
            files = [f for f in files if f['purpose'] == filter_purpose]

        logger.info(f"Found {len(files)} files to delete")

        if dry_run:
            logger.info("DRY RUN - No files will be deleted")
            for f in files:
                logger.info(f"  Would delete: {f['id']} ({f['filename']}) - {f['purpose']}")
            return {'dry_run': True, 'files_found': len(files), 'files': files}

        deleted = []
        failed = []

        for f in files:
            logger.info(f"Deleting: {f['id']} ({f['filename']})...")
            if self.delete_file(f['id']):
                deleted.append(f['id'])
            else:
                failed.append(f['id'])

        logger.info(f"Deleted {len(deleted)} files, {len(failed)} failed")

        return {
            'deleted': len(deleted),
            'failed': len(failed),
            'deleted_ids': deleted,
            'failed_ids': failed
        }

    def delete_all_vector_stores(self, dry_run: bool = False,
                                  filter_name: Optional[str] = None,
                                  delete_files: bool = True) -> Dict:
        """
        Delete all vector stores from OpenAI.

        Args:
            dry_run: If True, only show what would be deleted
            filter_name: Only delete stores with this name
            delete_files: If True, also delete files attached to stores

        Returns:
            Dictionary with deletion results
        """
        stores = self.list_all_vector_stores()

        if filter_name:
            stores = [s for s in stores if s['name'] == filter_name]

        logger.info(f"Found {len(stores)} vector stores to delete")

        if dry_run:
            logger.info("DRY RUN - No stores will be deleted")
            for s in stores:
                logger.info(f"  Would delete: {s['id']} ({s['name']}) - {s['file_counts']['total']} files")
            return {'dry_run': True, 'stores_found': len(stores), 'stores': stores}

        deleted = []
        failed = []
        total_files_deleted = 0

        for s in stores:
            logger.info(f"Deleting: {s['id']} ({s['name']})...")
            result = self.delete_vector_store(s['id'], delete_files=delete_files)
            if result['success']:
                deleted.append(s['id'])
                total_files_deleted += len(result.get('files_deleted', []))
            else:
                failed.append(s['id'])

        logger.info(f"Deleted {len(deleted)} stores, {len(failed)} failed")
        logger.info(f"Total files deleted: {total_files_deleted}")

        return {
            'stores_deleted': len(deleted),
            'stores_failed': len(failed),
            'files_deleted': total_files_deleted,
            'deleted_ids': deleted,
            'failed_ids': failed
        }

    def cleanup_all(self, dry_run: bool = False) -> Dict:
        """
        Delete ALL vector stores and files from OpenAI storage.

        Args:
            dry_run: If True, only show what would be deleted

        Returns:
            Dictionary with deletion results
        """
        logger.info("=" * 60)
        logger.info("OpenAI Storage Cleanup - DELETE ALL")
        logger.info("=" * 60)

        # Delete vector stores first (they reference files)
        stores_result = self.delete_all_vector_stores(dry_run=dry_run, delete_files=False)

        # Then delete all files
        files_result = self.delete_all_files(dry_run=dry_run)

        return {
            'vector_stores': stores_result,
            'files': files_result
        }

    def get_storage_summary(self) -> Dict:
        """Get a summary of current OpenAI storage usage."""
        files = self.list_all_files()
        stores = self.list_all_vector_stores()

        total_bytes = sum(f.get('bytes', 0) or 0 for f in files)

        # Group files by purpose
        by_purpose = {}
        for f in files:
            purpose = f['purpose']
            if purpose not in by_purpose:
                by_purpose[purpose] = {'count': 0, 'bytes': 0}
            by_purpose[purpose]['count'] += 1
            by_purpose[purpose]['bytes'] += f.get('bytes', 0) or 0

        return {
            'total_files': len(files),
            'total_bytes': total_bytes,
            'total_mb': round(total_bytes / (1024 * 1024), 2),
            'files_by_purpose': by_purpose,
            'total_vector_stores': len(stores),
            'vector_stores': stores,
            'files': files
        }

    def delete_file_by_name(self, filename: str) -> Dict:
        """
        Delete a specific file by filename.

        Args:
            filename: Name of the file to delete

        Returns:
            Dictionary with deletion results
        """
        files = self.list_all_files()
        matching = [f for f in files if f['filename'] == filename]

        if not matching:
            logger.warning(f"No file found with name: {filename}")
            return {'success': False, 'error': f'File not found: {filename}'}

        deleted = []
        failed = []

        for f in matching:
            logger.info(f"Deleting: {f['id']} ({f['filename']})...")
            if self.delete_file(f['id']):
                deleted.append(f['id'])
            else:
                failed.append(f['id'])

        return {
            'success': len(deleted) > 0,
            'deleted': len(deleted),
            'failed': len(failed),
            'deleted_ids': deleted
        }

    def delete_local_scraped_data(self) -> Dict:
        """
        Delete local scraped data files.

        Returns:
            Dictionary with deletion results
        """
        import shutil

        datasets_dir = Path.home() / "runtime_data" / "datasets" / "aws_reinvent_2025" / "latest-content"
        config_file = Path.home() / "runtime_data" / "keys" / "openai" / "vector-dbs" / "LLM-FineTuning-Solutions.json"

        deleted_items = []

        # Delete scraped data directory
        if datasets_dir.exists():
            try:
                shutil.rmtree(datasets_dir)
                deleted_items.append(str(datasets_dir))
                logger.info(f"Deleted: {datasets_dir}")
            except Exception as e:
                logger.error(f"Could not delete {datasets_dir}: {e}")
        else:
            logger.info(f"Directory not found (already deleted?): {datasets_dir}")

        # Delete config file
        if config_file.exists():
            try:
                config_file.unlink()
                deleted_items.append(str(config_file))
                logger.info(f"Deleted: {config_file}")
            except Exception as e:
                logger.error(f"Could not delete {config_file}: {e}")
        else:
            logger.info(f"Config file not found (already deleted?): {config_file}")

        return {
            'success': True,
            'deleted_items': deleted_items
        }

    def cleanup_everything(self, dry_run: bool = False) -> Dict:
        """
        Delete EVERYTHING: all OpenAI files, vector stores, and local scraped data.

        Args:
            dry_run: If True, only show what would be deleted

        Returns:
            Dictionary with deletion results
        """
        logger.info("=" * 60)
        logger.info("FULL CLEANUP - Delete ALL OpenAI Storage + Local Data")
        logger.info("=" * 60)

        if dry_run:
            # Show what would be deleted
            files = self.list_all_files()
            stores = self.list_all_vector_stores()

            datasets_dir = Path.home() / "runtime_data" / "datasets" / "aws_reinvent_2025" / "latest-content"
            config_file = Path.home() / "runtime_data" / "keys" / "openai" / "vector-dbs" / "LLM-FineTuning-Solutions.json"

            logger.info("DRY RUN - Nothing will be deleted")
            logger.info(f"\nWould delete from OpenAI:")
            logger.info(f"  - {len(stores)} vector stores")
            logger.info(f"  - {len(files)} files")
            logger.info(f"\nWould delete local:")
            logger.info(f"  - {datasets_dir} (exists: {datasets_dir.exists()})")
            logger.info(f"  - {config_file} (exists: {config_file.exists()})")

            return {
                'dry_run': True,
                'openai_stores': len(stores),
                'openai_files': len(files),
                'local_datasets_dir': str(datasets_dir),
                'local_config_file': str(config_file)
            }

        # Delete vector stores first
        stores_result = self.delete_all_vector_stores(dry_run=False, delete_files=False)

        # Delete all files from OpenAI
        files_result = self.delete_all_files(dry_run=False)

        # Delete local data
        local_result = self.delete_local_scraped_data()

        logger.info("=" * 60)
        logger.info("FULL CLEANUP COMPLETE!")
        logger.info(f"  Vector stores deleted: {stores_result.get('stores_deleted', 0)}")
        logger.info(f"  OpenAI files deleted: {files_result.get('deleted', 0)}")
        logger.info(f"  Local items deleted: {len(local_result.get('deleted_items', []))}")
        logger.info("=" * 60)

        return {
            'success': True,
            'vector_stores': stores_result,
            'openai_files': files_result,
            'local_data': local_result
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='OpenAI Storage Cleanup')
    parser.add_argument('action', choices=[
        'summary',
        'delete-files',
        'delete-file',
        'delete-stores',
        'delete-all',
        'cleanup-everything',
        'delete-local-data'
    ], help='Action to perform')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be deleted without actually deleting')
    parser.add_argument('--filter-name', type=str,
                        help='Only delete stores with this name')
    parser.add_argument('--filter-purpose', type=str,
                        help='Only delete files with this purpose (e.g., assistants)')
    parser.add_argument('--filename', type=str,
                        help='Specific filename to delete (for delete-file action)')
    parser.add_argument('--keep-files', action='store_true',
                        help='When deleting stores, keep the attached files')
    parser.add_argument('--json', action='store_true',
                        help='Output results as JSON')
    parser.add_argument('--force', action='store_true',
                        help='Skip confirmation prompts')

    args = parser.parse_args()

    try:
        manager = OpenAIStorageManager()

        if args.action == 'summary':
            result = manager.get_storage_summary()
            if args.json:
                print(json.dumps(result, indent=2, default=str))
            else:
                print("\n" + "=" * 60)
                print("OpenAI Storage Summary")
                print("=" * 60)
                print(f"\nTotal Files: {result['total_files']}")
                print(f"Total Size: {result['total_mb']} MB")
                print(f"\nFiles by Purpose:")
                for purpose, data in result['files_by_purpose'].items():
                    print(f"  {purpose}: {data['count']} files ({round(data['bytes']/(1024*1024), 2)} MB)")
                print(f"\nTotal Vector Stores: {result['total_vector_stores']}")
                for store in result['vector_stores']:
                    print(f"  - {store['name']} ({store['id']}): {store['file_counts']['total']} files")

        elif args.action == 'delete-files':
            result = manager.delete_all_files(
                dry_run=args.dry_run,
                filter_purpose=args.filter_purpose
            )
            if args.json:
                print(json.dumps(result, indent=2))
            elif not args.dry_run:
                print(f"\n✅ Deleted {result['deleted']} files")
                if result['failed'] > 0:
                    print(f"⚠️  Failed to delete {result['failed']} files")

        elif args.action == 'delete-file':
            if not args.filename:
                print("❌ Error: --filename is required for delete-file action")
                print("Usage: npm run openai:files:delete -- --filename=<filename>")
                sys.exit(1)
            result = manager.delete_file_by_name(args.filename)
            if args.json:
                print(json.dumps(result, indent=2))
            elif result['success']:
                print(f"\n✅ Deleted {result['deleted']} file(s) matching '{args.filename}'")
            else:
                print(f"\n❌ {result.get('error', 'Failed to delete file')}")

        elif args.action == 'delete-stores':
            result = manager.delete_all_vector_stores(
                dry_run=args.dry_run,
                filter_name=args.filter_name,
                delete_files=not args.keep_files
            )
            if args.json:
                print(json.dumps(result, indent=2))
            elif not args.dry_run:
                print(f"\n✅ Deleted {result['stores_deleted']} vector stores")
                print(f"✅ Deleted {result['files_deleted']} associated files")

        elif args.action == 'delete-all':
            if not args.dry_run and not args.force:
                print("\n⚠️  WARNING: This will delete ALL files and vector stores from OpenAI!")
                confirm = input("Type 'DELETE ALL' to confirm: ")
                if confirm != 'DELETE ALL':
                    print("Aborted.")
                    sys.exit(0)

            result = manager.cleanup_all(dry_run=args.dry_run)
            if args.json:
                print(json.dumps(result, indent=2))
            elif not args.dry_run:
                print(f"\n✅ Cleanup complete!")
                print(f"   Vector stores deleted: {result['vector_stores'].get('stores_deleted', 0)}")
                print(f"   Files deleted: {result['files'].get('deleted', 0)}")

        elif args.action == 'cleanup-everything':
            if not args.dry_run and not args.force:
                print("\n⚠️  WARNING: This will delete EVERYTHING:")
                print("   - ALL vector stores from OpenAI")
                print("   - ALL files from OpenAI storage")
                print("   - ALL local scraped data")
                print("   - Local vector DB config")
                confirm = input("\nType 'DELETE EVERYTHING' to confirm: ")
                if confirm != 'DELETE EVERYTHING':
                    print("Aborted.")
                    sys.exit(0)

            result = manager.cleanup_everything(dry_run=args.dry_run)
            if args.json:
                print(json.dumps(result, indent=2))
            elif not args.dry_run:
                print(f"\n✅ Full cleanup complete!")
                print(f"   Vector stores deleted: {result['vector_stores'].get('stores_deleted', 0)}")
                print(f"   OpenAI files deleted: {result['openai_files'].get('deleted', 0)}")
                print(f"   Local items deleted: {len(result['local_data'].get('deleted_items', []))}")

        elif args.action == 'delete-local-data':
            if not args.dry_run and not args.force:
                print("\n⚠️  WARNING: This will delete all local scraped data and config!")
                confirm = input("Type 'DELETE LOCAL' to confirm: ")
                if confirm != 'DELETE LOCAL':
                    print("Aborted.")
                    sys.exit(0)

            result = manager.delete_local_scraped_data()
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n✅ Local data cleanup complete!")
                for item in result.get('deleted_items', []):
                    print(f"   Deleted: {item}")

    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

