$(document).ready(function () {
    refresh;
    setInterval(refresh, 3000);
});

// auto refresh page
var notRefresh = false;
function refresh() {
    if (notRefresh) {
        return;
    }
    $.ajax({
        url: location.href,
        cache: false,
        dataType: "html",
        success: function (resp) {
            $(".sysinfo").html(resp);
        }
    });
}
