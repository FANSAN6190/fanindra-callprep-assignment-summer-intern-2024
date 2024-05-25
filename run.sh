echo "running in production mode"
source .venv/bin/activate
python3 main.py &
ngrok http --domain=pleasantly-winning-bluebird.ngrok-free.app 8040