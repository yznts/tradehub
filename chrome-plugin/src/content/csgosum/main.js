

$(document).ready(function () {
    LoadSettings(function(){
        API.setApiAddr(settings.API_ADDR, function(){});
        AddControls(function () {
            UpdateControls(()=>(null));
        });
    });
})