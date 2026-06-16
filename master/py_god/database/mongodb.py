import pymongo
from datetime import datetime
from config import Config

class DatabaseService:
    _client = None
    _db = None

    @classmethod
    def get_db(cls):
        """
        Lazily initialize the MongoDB client and return the database instance.
        Uses a short connection timeout to fail quickly if the database is not reachable.
        """
        if cls._db is not None:
            return cls._db

        mongo_uri = getattr(Config, "MONGO_URI", "mongodb://localhost:27017/screem")
        db_name = getattr(Config, "DB_NAME", "screem")

        if not mongo_uri:
            print("[Database] MONGO_URI is not set. Database operations disabled.")
            return None

        try:
            # Short timeout (2 seconds) so operations fail fast if DB is offline
            cls._client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
            cls._db = cls._client[db_name]
            # Ping database to verify active connection
            cls._client.admin.command('ping')
            print(f"[Database] Successfully connected to MongoDB database '{db_name}'")
            return cls._db
        except Exception as e:
            print(f"[Database] Failed to connect to MongoDB: {e}")
            cls._client = None
            cls._db = None
            return None

    @classmethod
    def save_completed_call(cls, session) -> bool:
        """
        Save the completed call session to MongoDB.
        The document keys are structured such that the memory parameters
        exist as top-level fields.
        """
        db = cls.get_db()
        if db is None:
            print("[Database] MongoDB client not connected. Skipping save.")
            return False

        try:
            # Get the memory dictionary representing all 17 fields
            memory_dict = session.memory.to_dict()

            # Merge memory fields, call_id, transcript, and full conversation history
            document = {
                "call_id": session.call_id,
                "timestamp": datetime.utcnow().isoformat(),
                "language": session.language,
                "preferred_language": getattr(session, "preferred_language", "english"),
                "messages": session.conversation.get_messages(),
                **memory_dict
            }

            collection = db["completed_calls"]
            
            # Upsert the record based on call_id
            collection.replace_one({"call_id": session.call_id}, document, upsert=True)
            print(f"[Database] Completed call {session.call_id} successfully persisted in MongoDB.")
            return True
        except Exception as e:
            print(f"[Database] Error occurred while saving call {session.call_id}: {e}")
            return False
