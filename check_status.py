import socket
import json
from datetime import datetime

# --- DATI DEL SERVER (AGGIORNATI) ---
# Formato: "Nome Server": ("IP o Domain", Porta)
SERVER_LIST = {
    # Questo indirizzo IP è quello del Game Server "TW Taipei" ricavato da ExitLag
    "Aion 2 TW - TW Taipei": ("210.242.123.91", 13700),  
    
    # Se trovi altri server (es. un server di login o altri server di gioco), 
    # aggiungili qui con i loro IP e porte
    # "Aion 2 TW - Nemon": ("XXX.XXX.XXX.XXX", 12345),
}
# ----------------------------------------

TIMEOUT = 3  # Timeout in secondi per il tentativo di connessione
STATUS_FILE = "server_status.json"

def check_server_status(ip, port):
    """Controlla se la porta TCP è aperta."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    try:
        # Tenta la connessione
        result = sock.connect_ex((ip, port))
        sock.close()
        
        # Se 0, la connessione è riuscita -> Online
        if result == 0:
            return "✅ Online"
        else:
            return "❌ Offline"
    except Exception:
        return "❌ Offline"

def run_check():
    results = {}
    
    for name, (ip, port) in SERVER_LIST.items():
        status = check_server_status(ip, port)
        results[name] = {
            "status": status,
            "ip_port": f"{ip}:{port}",
            "last_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        print(f"Server {name}: {status}")

    # Salva i risultati in un file JSON
    with open(STATUS_FILE, 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    run_check()
