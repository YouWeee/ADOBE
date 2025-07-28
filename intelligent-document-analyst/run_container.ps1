# PowerShell script to run the intelligent document analyst container
# This script ensures proper volume mounting for Windows

Write-Host "Starting Intelligent Document Analyst Container..." -ForegroundColor Green
Write-Host "Input directory: $PWD\input" -ForegroundColor Yellow
Write-Host "Output directory: $PWD\output" -ForegroundColor Yellow

# Remove any existing container with the same name
docker rm -f intelligent-analyst 2>$null

# Run the container with proper volume mounts
docker run --name intelligent-analyst --rm `
    -v "${PWD}/input:/app/input" `
    -v "${PWD}/output:/app/output" `
    --network none `
    mysolutionname:somerandomidentifier

Write-Host "Container execution completed!" -ForegroundColor Green
