

// Hide/open buttons
$("#access-settings-trigger").click(function () {
    ToggleOptions(function(){});
});
$("#commissions-settings-trigger").click(function () {
    ToggleCommissions(function(){});
});

// Current game update
var games = [];
PipePopup.addActionListener("update:games", function(data) {
    games = data;
    UpdateGamesList(games, function () {
        console.log("Games list updated from content script ", games);
    });
})

// Current service update
var codename = "";
var fullname = "";
PipePopup.addActionListener("update:codename", function (data) {
    codename = data;
    console.log("Codename updated from content script ", codename);
})
PipePopup.addActionListener("update:fullname", function (data) {
    fullname = data;
    console.log("Codename updated from content script ", fullname);
    $("#current-service").text(fullname.toUpperCase());
    $("#button-update").removeClass("pure-button-disabled");
    console.log("S2 updated");
})

// Server input binding
$("#server-address").on("input", function () {
    
    // Update value
    settings.API_ADDR = $("#server-address").val();
    API.setApiAddr(settings.API_ADDR, function(){});

    // Set input incorrect
    SetFieldRed("#server-address", function () {
        DisableTrade(function(){});
    });

    // Set input correct, save and sync settings
    API.ping(function() {
        SetFieldGreen("#server-address", function () {
            EnableTrade(function(){});
            SaveSettings(function(){});
            SyncSettings(function(){});
        })
    });

})

// Commissions bindings
$(".commission").on("input", function () {
    FieldsToSettings(function () {
        SaveSettings(function(){
            SyncSettings(function(){});
        });
    })
})


// Select bindings
$("#compare-game").on("change", function () {
    FieldsToSettings(function(){});
    SaveSettings(function(){
        SyncSettings(function(){});
    });
    API.getAvServices($(this).val(), function (services) {
        UpdateServicesList(services, function(){});
    })
});
// Select bindings
$("#compare-service").on("change", function () {
    FieldsToSettings(function(){});
    SaveSettings(function(){
        SyncSettings(function(){});
    });
});

$("#button-update").click(function () {
    PipePopup.sendMessage("update:rates", null, function(){});
})
$("#sort-s1-s2").click(function () {
    PipePopup.sendMessage("sort:s1-s2", null, ()=>(null));
})
$("#sort-s2-s1").click(function () {
    PipePopup.sendMessage("sort:s2-s1", null, ()=>(null));
})