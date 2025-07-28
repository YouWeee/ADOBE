@echo off
echo Starting Intelligent Document Analyst Container...
echo Input directory: %cd%\input
echo Output directory: %cd%\output

REM Remove any existing container with the same name
docker rm -f intelligent-analyst 2>nul

REM Run the container with proper volume mounts
docker run --name intelligent-analyst --rm ^
    -v "%cd%/input:/app/input" ^
    -v "%cd%/output:/app/output" ^
    --network none ^
    mysolutionname:somerandomidentifier

echo Container execution completed!
pause
