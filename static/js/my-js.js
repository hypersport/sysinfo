$(document).ready(function () {
    setInterval(refresh, 3000);
});
// auto refresh page
var autoRefresh = false;
function refresh() {
    if (autoRefresh) {
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