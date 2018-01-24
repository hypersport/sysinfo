function getInfoData(part, chart) {
    var infoData = 0;
    var part = part || 'cpu';
    var chart = chart || 'line';
    $.ajax({
        url: "http://127.0.0.1:9468/api/" + part + "/" + chart,
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