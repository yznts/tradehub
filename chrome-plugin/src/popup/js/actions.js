


// --------------
// Settings-related
// --------------

function FieldsToSettings(callback) {
    settings.API_ADDR = $("#server-address").val();
    settings.game = $("#compare-game").val();
    settings.s1 = $("#compare-service").val();
    settings.s1_commission = $("#s1-commission").val();
    settings.s2_commission = $("#s2-commission").val();
    callback();
}

function SettingsToFields(callback) {
    $("#server-address").val(settings.API_ADDR);
    $("#compare-game").val(settings.game);
    $("#compare-service").val(settings.s1);
    $("#s1-commission").val(settings.s1_commission);
    $("#s2-commission").val(settings.s2_commission);
    callback();
}



// --------------
// UI-only(!!!)
// --------------

function ToggleOptions(callback) {
    $("#access-settings-block").slideToggle();
    callback();
}

function ToggleCommissions(callback) {
    $("#commissions-settings-block").slideToggle();
    callback();
}

function SetFieldGreen(id, callback) {
    $(id).removeClass("input-bad");
    $(id).removeClass("input-good");
    $(id).addClass("input-good");
    callback();
}

function SetFieldRed(id, callback) {
    $(id).removeClass("input-bad");
    $(id).removeClass("input-good");
    $(id).addClass("input-bad");
    callback();
}

function EnableTrade(callback) {
    $("#trade-block").slideDown();
    callback();
}

function DisableTrade(callback) {
    $("#trade-block").slideUp();
    callback();
}

function UpdateGamesList(games, callback) {
    $("#compare-game").innerText = "";
    $.each(games, function (index, game) {
        $("#compare-game").append(
            $("<option>", {
                value: game,
                text: game
            })
        );
    })
}

function UpdateServicesList(services, callback) {
    $("#compare-service").html("");
    $.each(services, function (fullname, codename) {
        $("#compare-service").append(
            $("<option>", {
                value: fullname,
                text: fullname
            })
        );
    });
    callback();
}
