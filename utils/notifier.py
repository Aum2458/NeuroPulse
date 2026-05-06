from flask_socketio import SocketIO
from datetime import datetime
from typing import Optional, Dict

# -------------------------------------------------
# Global SocketIO instance (initialized from app.py)
# -------------------------------------------------
socketio_instance: Optional[SocketIO] = None

# -------------------------------------------------
# Initialization
# -------------------------------------------------
def init_socketio(sock: SocketIO) -> None:
    """
    Initialize the global SocketIO instance.

    Must be called once from app.py after `socketio = SocketIO(app)`.
    """
    global socketio_instance
    socketio_instance = sock
    log("✅ SocketIO initialized successfully.")

# -------------------------------------------------
# Real-time Event Emitter
# -------------------------------------------------
def send_alert(
    event_name: str,
    data: Dict,
    room: Optional[str] = None,
    namespace: Optional[str] = None
) -> None:
    """
    Emit a real-time Socket.IO event safely.

    Args:
        event_name (str): Event name (e.g., 'emergency_alert')
        data (Dict): Payload data
        room (Optional[str]): Target room (user_id / doctor_id)
        namespace (Optional[str]): Socket.IO namespace
    """
    if socketio_instance is None:
        log(f"❌ SocketIO not initialized. Event '{event_name}' not sent.")
        return

    if not isinstance(data, dict):
        log(f"❌ Invalid payload for event '{event_name}'. Must be dict.")
        return

    try:
        socketio_instance.emit(
            event_name,
            data,
            room=room,
            namespace=namespace
        )
        log(f"📢 Event Sent | Event='{event_name}' | Room='{room}' | Data={data}")
    except Exception as e:
        log(f"⚠️ SocketIO emit failed for '{event_name}': {e}")

# -------------------------------------------------
# Utilities
# -------------------------------------------------
def log(message: str) -> None:
    """Prints timestamped logs for monitoring."""
    print(f"[{current_time()}] {message}")

def current_time() -> str:
    """Returns formatted timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
