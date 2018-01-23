function getInfoData(part, shape) {
    var infoData = 0;
    var part = part || 'cpu';
    var shape = shape || 'line';
    $.ajax({
        url: "http://127.0.0.1:9468/api/" + part + "/" + shape,
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