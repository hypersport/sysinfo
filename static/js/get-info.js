function getInfoData(part, chart) {
    var infoData = 0;
    var part = part || 'cpu';
    var chart = chart || 'line';
    var fullPath = window.location.href;
    var pathName = window.location.pathname;
    var host = fullPath.substring(0, fullPath.indexOf(pathName));
    $.ajax({
        url: host + "/api/" + part + "/" + chart,
        cache: false,
        async: false,
        dataType: "json",
        success: function (data) {
            infoData = data;
        }
    });
    // console.log(infoData);
    return infoData;
}