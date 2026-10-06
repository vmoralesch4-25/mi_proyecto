const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let backendProcess;

function getBackendPath() {
  if (app.isPackaged) {
    return path.join(process.resourcesPath, 'backend', 'handsup-backend.exe');
  }
  return path.join(__dirname, '..', 'python-backend', 'dist', 'handsup-backend', 'handsup-backend.exe');
}

function startBackend() {
  const backendPath = getBackendPath();
  console.log('Iniciando backend desde:', backendPath);
  
  backendProcess = spawn(backendPath, [], { windowsHide: true });

  backendProcess.stdout.on('data', (data) => {
    console.log(`Backend Log: ${data}`);
  });

  backendProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`);
  });
}

function stopBackend() {
  if (backendProcess) {
    backendProcess.kill();
  }
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true
    }
  });

  win.loadFile('renderer/index.html');
}

app.whenReady().then(() => {
  startBackend();
  setTimeout(createWindow, 2000); // Espera 2 segundos para dar tiempo al servidor de arrancar
});

app.on('window-all-closed', () => {
  stopBackend();
  app.quit();
});