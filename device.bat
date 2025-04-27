@echo off
echo ===============================
echo Disconnecting old ADB connections...
adb disconnect

echo Restarting ADB in TCP/IP mode on port 5555...
adb tcpip 5555

echo Waiting for device to initialize...
timeout /t 3 /nobreak >nul

:: Get IP address from connected device (assumes connected via USB)
FOR /F "tokens=2" %%G IN ('adb shell ip addr show wlan0 ^| findstr "inet "') DO set ipfull=%%G
FOR /F "tokens=1 delims=/" %%G in ("%ipfull%") DO set DEVICE_IP=%%G

echo Detected device IP: %DEVICE_IP%
echo Connecting to device at %DEVICE_IP%:5555...
adb connect %DEVICE_IP%:5555

echo ===============================
echo Connection process finished.
pause

