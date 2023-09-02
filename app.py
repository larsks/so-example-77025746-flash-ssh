import subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/api/v1/remote/config")
def ssh_show_config():
    user = request.args.get("user")
    host = request.args.get("host")
    node = request.args.get("node")
    return jsonify(get_config_via_ssh(user, host, node))


# Note that I've replaced /storage/config with /tmp/config here; you'll
# want to swap that back to match the original code.
def get_config_via_ssh(user, host, tunnel_ip):
    try:
        cmd = [
            "ssh",
            "-A",
            "-J", f"{user}@{host}",
            f"root@{tunnel_ip}",
            "cat /tmp/config",
        ]

        # This will either work, or it will raise a CalledProcessError exception
        # (that will have .stdout and .stderr attributes available if we want
        # to pass any error messages to the caller).
        config = subprocess.check_output(cmd, encoding="utf-8", stderr=subprocess.PIPE)
        return {"config": config}
    except Exception as e:
        return {"error": f"Cannot connect to the device SSH Server: {e}"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
