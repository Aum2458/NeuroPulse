# socketio_instance.py
from flask_socketio import SocketIO

# -------------------- SOCKET.IO INSTANCE --------------------
# Initialize SocketIO with CORS allowed for all origins (safe for development)
socketio = SocketIO(cors_allowed_origins="*")

# -------------------- INIT FUNCTION --------------------
def init_socketio(app):
    """
    Attach SocketIO to the Flask app context.
    Call this in app.py after initializing Flask app.
    Example: init_socketio(app)
    """
    socketio.init_app(app)

# -------------------- REAL-TIME ALERT --------------------
def send_alert(event_name: str, data: dict):
    """
    Emit a real-time alert to connected clients.
    - event_name: e.g., 'risk_alert', 'timeline_update'
    - data: dictionary including user_id/username and risk info
    """
    try:
        socketio.emit(event_name, data)
        print(f"[SocketIO] Event '{event_name}' sent: {data}")
    except Exception as e:
        print(f"[SocketIO] Failed to emit event '{event_name}': {e}")
