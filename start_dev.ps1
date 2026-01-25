Write-Host "Starting GameMilano Development Environment..."

# Activate conda environment and start backend
Write-Host "Starting Backend (Python FastAPI)..."
Start-Process -FilePath "powershell" -ArgumentList "-Command", "& conda.bat activate 'e:\AIcoding\gamemilano\.conda'; python -m backend.main"

# Start Frontend
Write-Host "Starting Frontend (Vite)..."
Start-Process -FilePath "npm" -ArgumentList "run dev"

Write-Host "Services started in separate windows."
