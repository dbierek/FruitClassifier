#!/bin/bash
echo "Starting gunicorn..."
gunicorn --certfile cert.pem --keyfile privkey.pem --bind 0.0.0.0:5000 app:app &
GUNICORN_PID=$!
echo $GUNICORN_PID > gunicorn.pid
echo "Gunicorn started with PID: $GUNICORN_PID"

echo "Starting monitoring loop..."
while true; do
    echo "Sleeping for 20 minutes..."
    sleep 1200 # 20 minutes = 1200 seconds

    echo "Pinging server at http://localhost:5000/fruit-classifier..."
    curl --max-time 10 http://localhost:5000/fruit-classifier # 10 second timeout
    CURL_EXIT_CODE=$?

    # Curl exit codes:
    # 0: success
    # 28: operation timeout
    # For other non-zero codes, we might also want to restart, but the request specifically mentions timeout.
    # We'll consider any non-zero exit code as a failure for robustness.

    if [ $CURL_EXIT_CODE -ne 0 ]; then
        echo "Curl command failed with exit code $CURL_EXIT_CODE. Restarting gunicorn..."

        # Kill the old gunicorn process
        if [ -f gunicorn.pid ]; then
            OLD_PID=$(cat gunicorn.pid)
            echo "Killing gunicorn process with PID: $OLD_PID"
            kill $OLD_PID
            # Wait a bit for the process to terminate
            sleep 5
            # Check if process is still alive, if so, force kill
            if ps -p $OLD_PID > /dev/null; then
                echo "Process $OLD_PID still alive. Forcing kill..."
                kill -9 $OLD_PID
            fi
            rm gunicorn.pid
        else
            echo "gunicorn.pid file not found. Searching for gunicorn process to kill..."
            # Fallback: try to find and kill gunicorn processes if pid file is missing
            pkill -f "gunicorn.*app:app"
            sleep 2 # Give pkill some time
        fi

        # Restart gunicorn
        echo "Restarting gunicorn..."
        gunicorn --certfile cert.pem --keyfile privkey.pem --bind 0.0.0.0:5000 app:app &
        NEW_GUNICORN_PID=$!
        echo $NEW_GUNICORN_PID > gunicorn.pid
        echo "Gunicorn restarted with new PID: $NEW_GUNICORN_PID"
    else
        echo "Server is responsive."
    fi
done

#
# == Manual Testing Steps ==
#
# 1. Prerequisites:
#    - Ensure you have a dummy 'app:app' (e.g., a simple Flask app) that gunicorn can run and that it has a '/fruit-classifier' endpoint.
#    - Ensure 'cert.pem' and 'privkey.pem' exist in the same directory as the script, or adjust the gunicorn command if not using HTTPS or if files are elsewhere.
#    - Gunicorn and curl must be installed (`sudo apt-get install gunicorn curl`).
#    - The script must be executable (`chmod +x start_and_monitor_gunicorn.sh`).
#
# 2. Running the script:
#    ./start_and_monitor_gunicorn.sh
#
# 3. Verify initial gunicorn start:
#    - Check for "Starting gunicorn..." and "Gunicorn started with PID: <PID>" messages in the script's output.
#    - Check that 'gunicorn.pid' file is created in the current directory and contains a PID.
#    - Use 'ps aux | grep gunicorn' or 'pgrep -fl gunicorn' to see the running gunicorn process.
#    - You can also try accessing the server, e.g., `curl http://localhost:5000/fruit-classifier` (if not using HTTPS for gunicorn or if testing locally without SSL termination).
#      If using the provided certs, try `curl --cacert cert.pem https://localhost:5000/fruit-classifier` or access via browser, accepting self-signed cert.
#
# 4. Observe monitoring:
#    - The script will output "Starting monitoring loop..."
#    - Then "Sleeping for 20 minutes..."
#    - Followed by "Pinging server at http://localhost:5000/fruit-classifier..."
#    - If your app at /fruit-classifier is running and responsive, it will say "Server is responsive."
#    - (For faster testing, you can temporarily reduce the 'sleep 1200' duration in the script, e.g., to 'sleep 10').
#
# 5. Simulate a server timeout/hang:
#    Wait for the script to enter the "Sleeping for 20 minutes..." phase to avoid race conditions with startup.
#    Option A: Pause the gunicorn process (Recommended for testing timeout)
#      - In another terminal, run: kill -STOP $(cat gunicorn.pid)
#      - This will make gunicorn unresponsive without killing it. The curl command in the script should then time out.
#    Option B: Kill the gunicorn process directly
#      - In another terminal, run: kill $(cat gunicorn.pid)
#      - This simulates a crash.
#    Option C: (If applicable to your app setup) Temporarily make the /fruit-classifier endpoint unresponsive or cause it to hang.
#      - For example, by introducing a long sleep in its code or by temporarily renaming the endpoint.
#
# 6. Verify gunicorn restart:
#    - After the next ping attempt (following the sleep period), the script should detect the failure.
#    - Look for messages like "Pinging server...", then "Curl command failed with exit code 28..." (for timeout) or other non-zero code.
#    - Then, "Restarting gunicorn...", "Killing gunicorn process with PID: <OLD_PID>", and "Gunicorn restarted with new PID: <NEW_PID>".
#    - The 'gunicorn.pid' file should be updated with the new PID.
#    - Use 'ps aux | grep gunicorn' or 'pgrep -fl gunicorn' to confirm the old process is gone and a new one is running with the new PID.
#
# 7. Cleanup (Optional):
#    - To stop the monitoring script, use Ctrl+C in its terminal.
#    - This will not automatically stop the gunicorn process started by the script.
#    - Manually kill the last running gunicorn process: kill $(cat gunicorn.pid)
#    - Remove the 'gunicorn.pid' file: rm gunicorn.pid
#