"""
Firebase client for state management and real-time data streaming.
Implements CRUD operations with error handling and connection pooling.
"""
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class FirebaseClient:
    """Firebase Firestore client with connection management"""
    
    _instance = None
    _db = None
    
    def