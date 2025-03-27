# Projekt-Struktur 
## OPC UA
Der Ordner enthält den `Client`, den `Server`, den `Image-Analyzer` sowie die Bilder (png, modifiziertes png, jpg, modifiziertes jpg). 

### Benötigte Tools & Packages
- Node
- Node-OPCUA (install using npm: `npm install node-opcua --unsafe-perms`)

### Verbindung aufbauen
Bevor der Server gestartet werden kann, muss ausgewählt werden, welches Bild auf dem Server hinterlegt sein soll. Dazu muss der `picturePath` in `Server.js` angepasst werden.
> `const picturePath = path.join(__dirname, "imagePath");`

Um eine Verbindung aufzubauen muss zunächst der Server gestartet werden.
> `node Server.js`

 In der Konsole steht die IP, auf der der Server läuft. Diese IP muss dann anschließend in Client.js an der markierten Stelle eingetragen werden.
> `const endpointUrl = "opc.tcp://xxx.xxx.xxx.xx:4334/UA/MyServer"`

Anschließend kann der Client gestartet werden.
> `node Client.js`

## Modbus TCP



