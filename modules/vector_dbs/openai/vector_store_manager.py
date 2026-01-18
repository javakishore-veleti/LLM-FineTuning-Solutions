#!/usr/bin/env python3
"""
OpenAI Vector Store Manager

Creates, updates, and manages OpenAI vector stores for the LLM-FineTuning-Solutions project.
Reads scraped content and creates embeddings using OpenAI's API.
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
VECTOR_STORE_NAME = "LLM-FineTuning-Solutions"
DATASETS_DIR = Path.home() / "runtime_data" / "datasets" / "aws_reinvent_2025" / "latest-content"
VECTOR_DB_CONFIG_DIR = Path.home() / "runtime_data" / "keys" / "openai" / "vector-dbs"
CONFIG_FILE = VECTOR_DB_CONFIG_DIR / f"{VECTOR_STORE_NAME}.json"


class OpenAIVectorStoreManager:
    """Manager for OpenAI Vector Stores."""

    def __init__(self, store_name: str = VECTOR_STORE_NAME):
        """
        Initialize the vector store manager.

        Args:
            store_name: Name for the vector store
        """
        self.store_name = store_name
        self.client = self._init_client()
        self.config_dir = VECTOR_DB_CONFIG_DIR
        self.config_file = self.config_dir / f"{store_name}.json"
        self.datasets_dir = DATASETS_DIR

        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

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

    def load_config(self) -> Optional[Dict]:
        """Load existing vector store configuration."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return None

    def save_config(self, config: Dict):
        """Save vector store configuration."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"Configuration saved to {self.config_file}")

    def get_existing_files_from_openai(self) -> Dict[str, str]:
        """
        Get all existing files from OpenAI storage.

        Returns:
            Dictionary mapping filename to file_id
        """
        try:
            files = self.client.files.list()
            existing = {}
            for f in files.data:
                # Only consider files with purpose 'assistants' (for vector stores)
                if f.purpose == 'assistants':
                    existing[f.filename] = f.id
            logger.info(f"Found {len(existing)} existing files in OpenAI storage")
            return existing
        except Exception as e:
            logger.warning(f"Could not list files from OpenAI: {e}")
            return {}

    def get_content_files(self) -> List[Path]:
        """Get all content files from the datasets directory."""
        if not self.datasets_dir.exists():
            logger.error(f"Datasets directory not found: {self.datasets_dir}")
            logger.error("Please run 'npm run scrape:aws-reinvent' first.")
            return []

        # Get all .txt files except metadata
        files = [
            f for f in self.datasets_dir.glob("*.txt")
            if f.name != "scrape_metadata.json"
        ]

        logger.info(f"Found {len(files)} content files")
        return files

    def find_existing_store(self) -> Optional[Dict]:
        """Find existing vector store by name (checks OpenAI API, not just local config)."""
        # First check local config
        config = self.load_config()
        if config and 'vector_store_id' in config:
            try:
                store = self.client.vector_stores.retrieve(config['vector_store_id'])
                logger.info(f"Found existing vector store from config: {store.id}")
                return {
                    'id': store.id,
                    'name': store.name,
                    'file_counts': store.file_counts,
                    'source': 'config'
                }
            except Exception as e:
                logger.warning(f"Could not retrieve vector store from config: {e}")

        # Also check OpenAI for any stores with the same name (to prevent duplicates)
        try:
            logger.info(f"Checking OpenAI for existing vector stores named '{self.store_name}'...")
            stores = self.client.vector_stores.list()
            for store in stores.data:
                if store.name == self.store_name:
                    logger.info(f"Found existing vector store on OpenAI: {store.id}")
                    return {
                        'id': store.id,
                        'name': store.name,
                        'file_counts': store.file_counts,
                        'source': 'openai_api'
                    }
        except Exception as e:
            logger.warning(f"Could not list vector stores from OpenAI: {e}")

        return None

    def create_vector_store(self) -> Dict:
        """
        Create a new vector store and upload files.

        Returns:
            Dictionary with vector store details
        """
        logger.info("=" * 60)
        logger.info(f"Creating Vector Store: {self.store_name}")
        logger.info("=" * 60)

        # Check if store already exists
        existing = self.find_existing_store()
        if existing:
            logger.warning(f"Vector store already exists: {existing['id']}")
            logger.warning("Use 'npm run vectordb:update' to update or 'npm run vectordb:delete' to delete first.")
            return {
                'success': False,
                'error': 'Vector store already exists',
                'existing_store': existing
            }

        # Get content files
        files = self.get_content_files()
        if not files:
            return {
                'success': False,
                'error': 'No content files found'
            }

        # Get existing files from OpenAI to avoid duplicates
        logger.info("Checking for existing files in OpenAI storage...")
        existing_files = self.get_existing_files_from_openai()

        # Create vector store
        logger.info("Creating vector store...")
        vector_store = self.client.vector_stores.create(
            name=self.store_name
        )
        logger.info(f"Created vector store: {vector_store.id}")

        # Upload files and attach to vector store using create_and_poll
        uploaded_files = []
        reused_files = 0
        new_uploads = 0

        for file_path in files:
            try:
                # Check if file already exists in OpenAI storage
                if file_path.name in existing_files:
                    file_id = existing_files[file_path.name]
                    logger.info(f"♻️  Reusing existing file: {file_path.name} ({file_id})")
                    reused_files += 1
                else:
                    # Upload new file to OpenAI Files API with purpose="assistants"
                    logger.info(f"📤 Uploading new file: {file_path.name}")
                    with open(file_path, 'rb') as f:
                        file_obj = self.client.files.create(
                            file=f,
                            purpose='assistants'  # Important: must be 'assistants' for vector stores
                        )
                    file_id = file_obj.id
                    logger.info(f"Uploaded file: {file_id}")
                    new_uploads += 1

                # Attach file to vector store and poll until complete
                logger.info(f"Attaching to vector store and polling...")
                vs_file = self.client.vector_stores.files.create_and_poll(
                    vector_store_id=vector_store.id,
                    file_id=file_id
                )

                # Check status
                if vs_file.status == 'completed':
                    logger.info(f"✅ File attached successfully: {file_path.name}")
                else:
                    logger.warning(f"⚠️ File status: {vs_file.status}, error: {getattr(vs_file, 'last_error', None)}")

                uploaded_files.append({
                    'file_id': file_id,
                    'vs_file_id': vs_file.id if hasattr(vs_file, 'id') else file_id,
                    'filename': file_path.name,
                    'filepath': str(file_path),
                    'status': vs_file.status,
                    'reused': file_path.name in existing_files,
                    'uploaded_at': datetime.now().isoformat()
                })

            except Exception as e:
                logger.error(f"Failed to upload/attach {file_path.name}: {e}")

        # Count successful uploads
        successful_uploads = [f for f in uploaded_files if f.get('status') == 'completed']
        logger.info(f"Successfully attached {len(successful_uploads)}/{len(uploaded_files)} files to vector store")
        logger.info(f"  - New uploads: {new_uploads}")
        logger.info(f"  - Reused existing: {reused_files}")

        # Save configuration
        config = {
            'vector_store_name': self.store_name,
            'vector_store_id': vector_store.id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'datasets_directory': str(self.datasets_dir),
            'total_files': len(uploaded_files),
            'new_uploads': new_uploads,
            'reused_files': reused_files,
            'files': uploaded_files
        }

        self.save_config(config)

        logger.info("=" * 60)
        logger.info("Vector Store Creation Complete!")
        logger.info(f"Store ID: {vector_store.id}")
        logger.info(f"Total files: {len(uploaded_files)}")
        logger.info(f"  - New uploads: {new_uploads}")
        logger.info(f"  - Reused existing: {reused_files}")
        logger.info(f"Config saved to: {self.config_file}")
        logger.info("=" * 60)

        return {
            'success': True,
            'vector_store_id': vector_store.id,
            'vector_store_name': self.store_name,
            'files_uploaded': len(uploaded_files),
            'new_uploads': new_uploads,
            'reused_files': reused_files,
            'config_file': str(self.config_file)
        }

    def update_vector_store(self) -> Dict:
        """
        Update existing vector store with new/changed files.

        Returns:
            Dictionary with update results
        """
        logger.info("=" * 60)
        logger.info(f"Updating Vector Store: {self.store_name}")
        logger.info("=" * 60)

        config = self.load_config()
        if not config or 'vector_store_id' not in config:
            logger.error("No existing vector store found. Please create one first.")
            return {
                'success': False,
                'error': 'Vector store not found. Run npm run vectordb:create first.'
            }

        vector_store_id = config['vector_store_id']

        # Verify store exists
        try:
            store = self.client.vector_stores.retrieve(vector_store_id)
            logger.info(f"Found vector store: {store.id}")
        except Exception as e:
            logger.error(f"Vector store not found: {e}")
            return {
                'success': False,
                'error': f'Vector store not found: {e}'
            }

        # Get current files in store
        existing_file_ids = set(f['file_id'] for f in config.get('files', []))

        # Get content files
        files = self.get_content_files()
        if not files:
            return {
                'success': False,
                'error': 'No content files found'
            }

        # Get existing files from OpenAI to avoid duplicates
        logger.info("Checking for existing files in OpenAI storage...")
        openai_existing_files = self.get_existing_files_from_openai()

        # Upload new files using create_and_poll
        new_files = []
        reused_files = 0
        new_uploads = 0

        # Map existing filenames to file_ids from config
        existing_filenames = {f['filename']: f['file_id'] for f in config.get('files', [])}

        for file_path in files:
            # Check if file is already in the vector store (from config)
            if file_path.name not in existing_filenames:
                try:
                    # Check if file already exists in OpenAI storage
                    if file_path.name in openai_existing_files:
                        file_id = openai_existing_files[file_path.name]
                        logger.info(f"♻️  Reusing existing file: {file_path.name} ({file_id})")
                        reused_files += 1
                    else:
                        # Upload file with purpose='assistants'
                        logger.info(f"📤 Uploading new file: {file_path.name}")
                        with open(file_path, 'rb') as f:
                            file_obj = self.client.files.create(
                                file=f,
                                purpose='assistants'  # Important: must be 'assistants' for vector stores
                            )
                        file_id = file_obj.id
                        logger.info(f"Uploaded file: {file_id}")
                        new_uploads += 1

                    # Attach to vector store and poll until complete
                    logger.info(f"Attaching to vector store and polling...")
                    vs_file = self.client.vector_stores.files.create_and_poll(
                        vector_store_id=vector_store_id,
                        file_id=file_id
                    )

                    # Check status
                    if vs_file.status == 'completed':
                        logger.info(f"✅ File attached successfully: {file_path.name}")
                    else:
                        logger.warning(f"⚠️ File status: {vs_file.status}, error: {getattr(vs_file, 'last_error', None)}")

                    new_files.append({
                        'file_id': file_id,
                        'vs_file_id': vs_file.id if hasattr(vs_file, 'id') else file_id,
                        'filename': file_path.name,
                        'filepath': str(file_path),
                        'status': vs_file.status,
                        'reused': file_path.name in openai_existing_files,
                        'uploaded_at': datetime.now().isoformat()
                    })

                except Exception as e:
                    logger.error(f"Failed to upload {file_path.name}: {e}")

        # Update configuration
        config['files'].extend(new_files)
        config['updated_at'] = datetime.now().isoformat()
        config['total_files'] = len(config['files'])

        self.save_config(config)

        # Count successful uploads
        successful_uploads = [f for f in new_files if f.get('status') == 'completed']

        logger.info("=" * 60)
        logger.info("Vector Store Update Complete!")
        logger.info(f"New files added: {len(successful_uploads)}/{len(new_files)}")
        logger.info(f"  - New uploads: {new_uploads}")
        logger.info(f"  - Reused existing: {reused_files}")
        logger.info(f"Total files: {config['total_files']}")
        logger.info("=" * 60)

        return {
            'success': True,
            'vector_store_id': vector_store_id,
            'new_files_added': len(new_files),
            'new_uploads': new_uploads,
            'reused_files': reused_files,
            'total_files': config['total_files']
        }

    def delete_vector_store(self, delete_all_duplicates: bool = True) -> Dict:
        """
        Delete the vector store and associated files.
        Also cleans up any duplicate stores with the same name on OpenAI.

        Args:
            delete_all_duplicates: If True, delete ALL vector stores with this name on OpenAI

        Returns:
            Dictionary with deletion results
        """
        logger.info("=" * 60)
        logger.info(f"Deleting Vector Store: {self.store_name}")
        logger.info("=" * 60)

        deleted_stores = []
        deleted_files = []

        # Delete from local config first
        config = self.load_config()
        if config and 'vector_store_id' in config:
            vector_store_id = config['vector_store_id']

            # Delete files from OpenAI
            for file_info in config.get('files', []):
                try:
                    self.client.files.delete(file_info['file_id'])
                    deleted_files.append(file_info['file_id'])
                    logger.info(f"Deleted file: {file_info['file_id']}")
                except Exception as e:
                    logger.warning(f"Could not delete file {file_info['file_id']}: {e}")

            # Delete vector store
            try:
                self.client.vector_stores.delete(vector_store_id)
                deleted_stores.append(vector_store_id)
                logger.info(f"Deleted vector store: {vector_store_id}")
            except Exception as e:
                logger.warning(f"Could not delete vector store {vector_store_id}: {e}")

            # Remove config file
            if self.config_file.exists():
                self.config_file.unlink()
                logger.info(f"Removed config file: {self.config_file}")

        # Also delete any other stores with the same name on OpenAI (cleanup duplicates)
        if delete_all_duplicates:
            logger.info(f"Checking for duplicate vector stores named '{self.store_name}'...")
            try:
                stores = self.client.vector_stores.list()
                for store in stores.data:
                    if store.name == self.store_name and store.id not in deleted_stores:
                        try:
                            # Delete files attached to this store
                            try:
                                vs_files = self.client.vector_stores.files.list(vector_store_id=store.id)
                                for vs_file in vs_files.data:
                                    try:
                                        self.client.files.delete(vs_file.id)
                                        deleted_files.append(vs_file.id)
                                        logger.info(f"Deleted file from duplicate store: {vs_file.id}")
                                    except Exception as e:
                                        logger.warning(f"Could not delete file {vs_file.id}: {e}")
                            except Exception as e:
                                logger.warning(f"Could not list files for store {store.id}: {e}")

                            self.client.vector_stores.delete(store.id)
                            deleted_stores.append(store.id)
                            logger.info(f"Deleted duplicate vector store: {store.id}")
                        except Exception as e:
                            logger.warning(f"Could not delete duplicate store {store.id}: {e}")
            except Exception as e:
                logger.warning(f"Could not check for duplicates: {e}")

        logger.info("=" * 60)
        logger.info("Vector Store Deletion Complete!")
        logger.info(f"Stores deleted: {len(deleted_stores)}")
        logger.info(f"Files deleted: {len(deleted_files)}")
        logger.info("=" * 60)

        return {
            'success': True,
            'stores_deleted': deleted_stores,
            'files_deleted': len(deleted_files)
        }

    def get_status(self) -> Dict:
        """
        Get the current status of the vector store.

        Returns:
            Dictionary with status information
        """
        config = self.load_config()

        if not config:
            return {
                'exists': False,
                'message': 'No vector store configured'
            }

        # Try to get store details from OpenAI
        try:
            store = self.client.vector_stores.retrieve(config['vector_store_id'])
            return {
                'exists': True,
                'vector_store_id': store.id,
                'vector_store_name': store.name,
                'file_counts': {
                    'in_progress': store.file_counts.in_progress,
                    'completed': store.file_counts.completed,
                    'failed': store.file_counts.failed,
                    'cancelled': store.file_counts.cancelled,
                    'total': store.file_counts.total
                },
                'created_at': config.get('created_at'),
                'updated_at': config.get('updated_at'),
                'local_files': len(config.get('files', []))
            }
        except Exception as e:
            return {
                'exists': False,
                'error': str(e),
                'config_exists': True,
                'config': config
            }


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='OpenAI Vector Store Manager')
    parser.add_argument('action', choices=['create', 'update', 'delete', 'status'],
                        help='Action to perform')
    parser.add_argument('--store-name', type=str, default=VECTOR_STORE_NAME,
                        help=f'Vector store name (default: {VECTOR_STORE_NAME})')

    args = parser.parse_args()

    try:
        manager = OpenAIVectorStoreManager(store_name=args.store_name)

        if args.action == 'create':
            result = manager.create_vector_store()
        elif args.action == 'update':
            result = manager.update_vector_store()
        elif args.action == 'delete':
            result = manager.delete_vector_store()
        elif args.action == 'status':
            result = manager.get_status()
            print(json.dumps(result, indent=2))
            return

        if result.get('success'):
            print(f"\n✅ {args.action.capitalize()} completed successfully!")
        else:
            print(f"\n❌ {args.action.capitalize()} failed: {result.get('error')}")
            sys.exit(1)

    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

