#!/bin/bash
# Helper script for rendering Manim animations
# Usage: ./render.sh [scene_name] [quality]
#
# Examples:
#   ./render.sh HelloManimTest      # Quick test (low quality)
#   ./render.sh NeuralNetworkScene  # Main animation
#   ./render.sh NeuralNetworkScene high  # High quality 1080p

cd "$(dirname "$0")"
source venv/bin/activate

SCENE=${1:-HelloManimTest}
QUALITY=${2:-low}

case $QUALITY in
    low|l|ql)
        FLAGS="-pql"
        echo "Rendering $SCENE in LOW quality (480p, 15fps)..."
        ;;
    medium|m|qm)
        FLAGS="-pqm"
        echo "Rendering $SCENE in MEDIUM quality (720p, 30fps)..."
        ;;
    high|h|qh)
        FLAGS="-pqh"
        echo "Rendering $SCENE in HIGH quality (1080p, 60fps)..."
        ;;
    4k|k|qk)
        FLAGS="-pqk"
        echo "Rendering $SCENE in 4K quality (2160p, 60fps)..."
        ;;
    *)
        FLAGS="-pql"
        echo "Rendering $SCENE in LOW quality (default)..."
        ;;
esac

echo ""
manim $FLAGS neural_network.py $SCENE

echo ""
echo "Output saved to: media/videos/neural_network/"
