const { OPCUAClient, AttributeIds } = require("node-opcua");
const fs = require("fs");
const path = require("path");
const { analyzeImage } = require("./imageAnalyzer");

(async () => {
    const client = OPCUAClient.create({
        endpointMustExist: false,
    });

    const endpointUrl = "opc.tcp://xxx.xxx.xxx.xx:4334/UA/MyServer"; // Use Machine B's IP address here

    try {
        await client.connect(endpointUrl);
        console.log("Connected to server:", endpointUrl);

        const session = await client.createSession();
        console.log("Session created.");

        const nodeId = "ns=1;s=Picture";
        const dataValue = await session.read({
            nodeId,
            attributeId: AttributeIds.Value,
        });

        const pictureData = dataValue.value.value; // Base64 string
        const pictureBuffer = Buffer.from(pictureData, "base64");

        // Analyze the image for extra content
        const extraContent = analyzeImage(pictureBuffer);
        if (extraContent) {
            console.log(`Extra content found: "${extraContent}"`);
            console.log("Cancelling Download.");
        } else {
            console.log("No extra content found.");
            // Save the picture to a file
            const outputPath = path.join(__dirname, "downloaded_picture.png");
            fs.writeFileSync(outputPath, pictureBuffer);
            console.log("Picture saved at:", outputPath);
        }

        await session.close();
        console.log("Session closed.");
    } catch (err) {
        console.error("Error:", err);
    } finally {
        await client.disconnect();
        console.log("Client disconnected.");
    }
})();