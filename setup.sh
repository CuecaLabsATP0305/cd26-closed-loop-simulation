#!/usr/bin/env bash
set -e
echo "======================================================================"
echo "🔬 [CUECALABS] Inicializando Entorno Automatizado para Teléfonos..."
echo "======================================================================"
if ! command -v python3 &> /dev/null; then
    echo "❌ [ERROR] Python 3 no está instalado."
    exit 1
fi
python3 -m venv cuecalabs_env
source cuecalabs_env/bin/activate
echo "⚡ Instalando dependencias de producción y suite móvil (Streamlit)..."
pip install --upgrade pip
pip install numpy matplotlib streamlit
echo "======================================================================"
echo "✅ [CUECALABS] ¡Entorno configurado con éxito!"
echo "======================================================================"

