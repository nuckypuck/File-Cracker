const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('api', {
  selectWordlist: () => ipcRenderer.invoke('select-wordlist'),
  selectFile:    () => ipcRenderer.invoke('select-file'),
  startCrack:    (opts) => ipcRenderer.invoke('start-crack', opts),
  onUpdate:      (cb) => ipcRenderer.on('crack-update', (_e, line) => cb(line)),
  removeUpdates: () => ipcRenderer.removeAllListeners('crack-update'),
  cancelCrack:   () => ipcRenderer.invoke('cancel-crack')
})
