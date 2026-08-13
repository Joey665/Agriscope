#!/bin/bash
cd ~/agriscope
source venv/bin/activate

# Stop any existing services
pkill -f streamlit 2>/dev/null
pkill -f jupyter 2>/dev/null
pkill -f ngrok 2>/dev/null

# Start Streamlit
nohup streamlit run dashboard/app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    > logs/streamlit.log 2>&1 &

echo "⏳ Waiting for Streamlit to start..."
sleep 5

# Check if Streamlit is running
if curl -s http://localhost:8501 > /dev/null; then
    echo "✅ Streamlit is running on port 8501"
else
    echo "❌ Streamlit failed to start. Check logs/streamlit.log"
    tail -20 logs/streamlit.log
    exit 1
fi

# Start Jupyter
nohup jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root > logs/jupyter.log 2>&1 &
echo "✅ Jupyter started on port 8888"

# Start ngrok
nohup ngrok http 8501 > logs/ngrok.log 2>&1 &
echo "✅ ngrok started"

echo ""
echo "📊 Waiting for ngrok URL..."
sleep 5

# Get ngrok URL
curl -s http://127.0.0.1:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | head -1

echo ""
echo "📋 Logs:"
echo "  Streamlit: tail -f logs/streamlit.log"
echo "  ngrok: tail -f logs/ngrok.log"
