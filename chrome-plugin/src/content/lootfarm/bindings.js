

// Popup-related. Functional part

PipeContent.addActionListener("update:games", function () {
    PipeContent.sendMessage("update:games", GAMES, function(){});
});

PipeContent.addActionListener("update:codename", function () {
    PipeContent.sendMessage("update:codename", CODENAME, function(){});
});

PipeContent.addActionListener("update:fullname", function () {
    PipeContent.sendMessage("update:fullname", FULLNAME, function(){});
});

PipeContent.addActionListener("sync:settings", function (settings) {
    LoadSettings(function(){
        UpdateControls(()=>(null));
    });
})



// Content related

PipeContent.addActionListener("update:rates", function() {
    UpdateRates(function(){});
})
PipeContent.addActionListener("sort:s1-s2", function() {
    SortS1S2(()=>(null));
})
PipeContent.addActionListener("sort:s2-s1", function () {
    SortS2S1(()=>(null));
})