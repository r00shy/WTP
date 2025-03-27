const findIEND = (buffer) => {
    const IEND_MARKER = Buffer.from([0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82]);
    const index = buffer.indexOf(IEND_MARKER);
    return index !== -1 ? index + IEND_MARKER.length : -1; // Return byte index after the marker
};

const analyzeImage = (buffer) => {
    const iendEnd = findIEND(buffer);
    if (iendEnd !== -1 && buffer.length > iendEnd) {
        const extraContentBuffer = buffer.slice(iendEnd);
        return extraContentBuffer.toString("utf-8");
    }
    return null;
};

module.exports = { analyzeImage };