
from supabase import create_client, Client
from .config import config

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
