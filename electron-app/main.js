const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

let backendProcess;

function getBackendCommand() {
  // 1. App empaquetada: usa el .exe incluido en resources
  if (app.isPackaged) {
    return {
      cmd: path.join(process.resourcesPath, 'backend', 'handsup-backend.exe'),
      args: [],
      cwd: undefined
    };
  }

  // 2. Desarrollo con el .exe compilado, si existe
  const exePath = path.join(__dirname, '..', 'python-backend', 'dist', 'handsup-backend', 'handsup-backend.exe');
  if (fs.existsSync(exePath)) {
    return { cmd: exePath, args: [], cwd: undefined };
  }

  // 3. Desarrollo con Python directo (venv)
  const backendDir = path.join(__dirname, '..', 'python-backend');
  return {
    cmd: path.join(backendDir, 'venv', 'Scripts', 'python.exe'),
    args: [path.join('src', 'main.py')],
    cwd: backendDir
  };
}

function startBackend() {
  const { cmd, args, cwd } = getBackendCommand();
  console.log('Iniciando backend:', cmd, args.join(' '));

  backendProcess = spawn(cmd, args, { windowsHide: true, cwd });

  backendProcess.on('error', (err) => {
    console.error('No se pudo iniciar el backend:', err.message);
  });

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