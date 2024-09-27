# Multicast Data Monitor

This project implements a WebSocket server that listens for multicast UDP messages and forwards them to connected WebSocket clients. It allows real-time monitoring of multicast data through a web interface.
## Prerequisites

* Python 3.11
* `pip install -r requirements.txt`

## How to Run

1. Ensure you have Python 3.11 and the required packages installed. You can set up the environment using Nix with the provided `flake.nix`.
2. Run the server using the following command:
   ```bash
   just run
   ```
3. Open `web/index.html` in your browser to view the multicast data.
