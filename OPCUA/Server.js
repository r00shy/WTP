const {
	OPCUAServer,
	Variant,
	DataType,
	StatusCodes
} = require("node-opcua");
const fs = require("fs");
const os = require("os");
const path = require("path");

// Get the local IP address of Machine B
const ipAddress = Object.values(os.networkInterfaces())
	.flat()
	.find((iface) => iface.family === "IPv4" && !iface.internal).address;

(async () => {
const server = new OPCUAServer({
	port: 4334, // Default OPC UA port
        resourcePath: "/UA/MyServer",
        buildInfo: {
            productName: "PictureExchangeServer",
            buildNumber: "1",
            buildDate: new Date(),
        },
	hostname: ipAddress, // Use Machine B's IP address here
});
await server.initialize();

    const addressSpace = server.engine.addressSpace;
    const namespace = addressSpace.getOwnNamespace();

    const device = namespace.addObject({
        organizedBy: addressSpace.rootFolder.objects,
        browseName: "Device",
    });

    // Read the picture file and encode it in base64
    const picturePath = path.join(__dirname, "img_modified/trojanHorse.png"); // img_jpg_modified/cat.jpg   img/trojanHorse.png   img_modified/trojanHorse.png
    const pictureData = fs.readFileSync(picturePath).toString("base64");

    namespace.addVariable({
        componentOf: device,
        browseName: "Picture",
        nodeId: "ns=1;s=Picture", // Unique identifier
        dataType: "String",
        value: new Variant({ dataType: DataType.String, value: pictureData }),
    });

    await server.start();
    console.log("Server is running at:", server.endpoints[0].endpointDescriptions()[0].endpointUrl);

    process.on("SIGINT", async () => {
        console.log("Shutting down server...");
        await server.shutdown();
        console.log("Server shut down.");
        process.exit(0);
    });
})();
