#!/usr/bin/env bash
# ========================================================================================
#       CUECALABS QUANTUM PHARMACOLOGY SUITE — AUTOMATIZADOR DE ENTORNO CIENTÍFICO MÓVIL
#       Desplegado por: CuecaLabsATP0305
# ========================================================================================

set -e # Detiene la ejecución si ocurre algún error

echo "======================================================================"
echo "🔬 [CUECALABS] Inicializando Entorno Automatizado para Teléfonos..."
echo "======================================================================"

# 1. Verificar si Python 3 está instalado en el sistema
if ! command -v python3 &> /dev/null; then
    echo "❌ [ERROR] Python 3 no está instalado. Instálelo antes de continuar."
    exit 1
fi

# 2. Crear un entorno virtual aislado para evitar conflictos de librerías
echo "📦 Creando entorno virtual aislado (cuecalabs_env)..."
python3 -m venv cuecalabs_env

# 3. Activar el entorno virtual
echo "🚀 Activando entorno virtual..."
source cuecalabs_env/bin/activate

# 4. Actualizar pip e instalar dependencias bioestadísticas y suite interactiva móvil
echo "⚡ Instalando dependencias de producción y suite móvil (Streamlit)..."
pip install --upgrade pip
pip install numpy matplotlib streamlit

echo "======================================================================"
echo "✅ [CUECALABS] ¡Entorno configurado con éxito!"
echo "======================================================================"
