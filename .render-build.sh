#!/usr/bin/env bash
echo "Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt

echo "Instalando Chromium para Playwright..."
playwright install chromium
