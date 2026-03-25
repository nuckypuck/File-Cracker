const { app, BrowserWindow, ipcMain, dialog, Menu } = require('electron')
const path = require('path')
const { spawn } = require('child_process')
const fs = require('fs')

let mainWindow
let crackerProc = null

function createWindow () {
  mainWindow = new BrowserWindow({
    width: 860,
    height: 620,
    minWidth: 700,
    minHeight: 500,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    backgroundColor: '#f0f0ee',
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
    title: 'File Cracker — MDX Cyber Security Society'
  })

  Menu.setApplicationMenu(null)
  mainWindow.loadFile('index.html')
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})

// Open wordlist file picker
ipcMain.handle('select-wordlist', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [{ name: 'Wordlist', extensions: ['txt'] }]
  })
  return result.canceled ? null : result.filePaths[0]
})

// Open target file picker (fallback if drag-and-drop fails)
ipcMain.handle('select-file', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile']
  })
  return result.canceled ? null : result.filePaths[0]
})

// Run the cracker for the given file type
ipcMain.handle('start-crack', async (event, { filePath, wordlistPath, fileType }) => {
  const crackerScript = path.join(__dirname, 'crackers', `${fileType}.py`)

  if (!fs.existsSync(crackerScript)) {
    return { error: `No cracker found for .${fileType} — is crackers/${fileType}.py implemented?` }
  }

  return new Promise((resolve) => {
    const proc = spawn('python', [crackerScript, '--file', filePath, '--wordlist', wordlistPath])
    crackerProc = proc

    proc.stdout.on('data', (data) => {
      const lines = data.toString().split('\n').filter(l => l.trim())
      lines.forEach(line => {
        // Forward each stdout line to the renderer
        mainWindow.webContents.send('crack-update', line.trim())
      })
    })

    proc.stderr.on('data', (data) => {
      mainWindow.webContents.send('crack-update', `ERROR:${data.toString().trim()}`)
    })

    proc.on('close', () => {
      crackerProc = null
      resolve({ done: true })
    })
    proc.on('error', (err) => {
      crackerProc = null
      resolve({ error: err.message })
    })
  })
})

// Cancel the running cracker process
ipcMain.handle('cancel-crack', () => {
  if (crackerProc) {
    crackerProc.kill()
    crackerProc = null
  }
})
