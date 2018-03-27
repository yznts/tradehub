

flow.exec(

    // Receive data from content script
    function () { PipePopup.sendMessage("update:games", null, this) },
    function () { PipePopup.sendMessage("update:codename", null, this) },
    function () { PipePopup.sendMessage("update:fullname", null, this) },

    // Settings part
    function () { LoadSettings(this) },
    function () { SyncSettings(this) },
    function () { API.setApiAddr(settings.API_ADDR, this) },
    function () { SettingsToFields(this) },
    
    // Server info part
    function () { SetFieldRed("#server-input", this); },
    function () { API.ping(this) },
    function () { SetFieldGreen("#server-input", this); },
    function () { EnableTrade(this) },
    function () { API.getAvServices($("#compare-game").val(), this) },
    function (services) { UpdateServicesList(services, this) },
    function () { $("#compare-service").val(settings.s1) },

)