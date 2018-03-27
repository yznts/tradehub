

// Default values
var settings = {
    API_ADDR: "http://127.0.0.1:2087",
    s1_commission: 0,
    s2_commission: 0,
    game: undefined,
    s1: undefined,
}

function LoadSettings(callback) {
    // Load
    chrome.storage.local.get("settings", function (temp_settings) {
        // Save if not undefined
        if (temp_settings["settings"] !== undefined) {
            settings = temp_settings["settings"];
        }
        // Log
        console.log("Settings loaded: ", settings);
        // Callback
        callback();
    });
}

function SaveSettings(callback) {
    chrome.storage.local.set({"settings": settings}, function () {
        // Log
        console.log("Settings saved ", settings);
        // Callback
        callback();
    })
}

function SyncSettings(callback) {
    PipePopup.sendMessage("sync:settings", null, callback);
}