$(document).ready(function () {
    setInterval(refresh, 3000)
});

// auto refresh page
var notRefresh = true;

function refresh() {
    if (notRefresh) {
        return;
    }
    // window.location.href = location.href

    $.ajax({
        url: location.href,
        cache: false,
        dataType: "html",
        success: function (resp) {
            $(".sysinfo").html(resp);
        }
    });
}
