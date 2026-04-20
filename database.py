
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client() -> Client:
    """
    Creates and returns a Supabase client connection.
    This is like 'opening a connection' to the database.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "❌ Supabase credentials not found!\n"
            "Please make sure you have a .env file with:\n"
            "  SUPABASE_URL=your-url\n"
            "  SUPABASE_KEY=your-key\n"
            "See README.md for step-by-step setup instructions."
        )

    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase: Client = get_supabase_client()
    DB_CONNECTED = True
except ValueError as e:
    DB_CONNECTED = False
    DB_ERROR = str(e)

def insert_complaint(title: str, description: str, sentiment: str, urgency: str, priority: str) -> dict:
    """
    Saves a new complaint to the 'complaints' table in Supabase.

    Parameters:
        title       → The complaint title (e.g., "Internet Not Working")
        description → Full complaint details
        sentiment   → "Positive", "Neutral", or "Negative"
        urgency     → "High" or "Low"
        priority    → "Critical", "High", "Medium", or "Low"

    Returns:
        The saved complaint data if successful, or raises an error.
    """
    
    data = {
        "title": title,
        "description": description,
        "sentiment": sentiment,
        "urgency": urgency,
        "priority": priority,
        "status": "Pending"  # All new complaints start as Pending
    }

    response = supabase.table("complaints").insert(data).execute()
    return response.data[0] if response.data else {}

def fetch_all_complaints() -> list:
    """
    Retrieves ALL complaints from the database.
    Sorted so that most recently submitted appear first.

    Returns:
        A list of complaint dictionaries.
        Example: [
            {'id': 'abc123', 'title': 'Internet Down', 'priority': 'Critical', ...},
            {'id': 'def456', 'title': 'Billing Error', 'priority': 'High', ...},
        ]
    """

    response = (
        supabase
        .table("complaints")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return response.data if response.data else []

def fetch_filtered_complaints(priority_filter: str = "All", status_filter: str = "All") -> list:
    """
    Fetches complaints with optional filters for priority and status.

    Parameters:
        priority_filter → "All", "Critical", "High", "Medium", or "Low"
        status_filter   → "All", "Pending", "In Progress", or "Resolved"

    Returns:
        Filtered list of complaint dictionaries.
    """
    
    query = supabase.table("complaints").select("*")
    if priority_filter != "All":
        query = query.eq("priority", priority_filter)
    if status_filter != "All":
        query = query.eq("status", status_filter)
    query = query.order("created_at", desc=True)

    response = query.execute()
    complaints = response.data if response.data else []

   
    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}

    complaints.sort(key=lambda x: priority_order.get(x.get("priority", "Low"), 3))

    return complaints
def update_complaint_status(complaint_id: str, new_status: str) -> bool:
    """
    Updates the status of a complaint by its ID.

    Parameters:
        complaint_id → The unique ID of the complaint (UUID string)
        new_status   → "Pending", "In Progress", or "Resolved"

    Returns:
        True if update was successful, False otherwise.
    """
   
    response = (
        supabase
        .table("complaints")
        .update({"status": new_status})
        .eq("id", complaint_id)
        .execute()
    )

    return len(response.data) > 0
