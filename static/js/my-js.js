$(document).ready(function () {
    // for memory.html
    $("#memory-span").click(function () {
        $("#memory-span").css("color", "#000000");
        $("#memory-span").siblings().css("color", "#cccccc");
        $("#memory").siblings().hide();
        $("#memory").show();
    });
    $("#swap-span").click(function () {
        $("#swap-span").css("color", "#000000");
        $("#swap-span").siblings().css("color", "#cccccc");
        $("#swap-info").siblings().hide();
        $("#swap-info").show();
    });

    // for disks.html
    $("#disk-span").click(function () {
        $("#disk-span").css("color", "#000000");
        $("#disk-span").siblings().css("color", "#cccccc");
        $("#disks").siblings().hide();
        $("#disks").show();
    });
    $("#part-span").click(function () {
        $("#part-span").css("color", "#000000");
        $("#part-span").siblings().css("color", "#cccccc");
        $("#parts").siblings().hide();
        $("#parts").show();
    });
    $("#disk-io-span").click(function () {
        $("#disk-io-span").css("color", "#000000");
        $("#disk-io-span").siblings().css("color", "#cccccc");
        $("#disk-io").siblings().hide();
        $("#disk-io").show();
    });

    // for network.html
    $("#network-span").click(function () {
        $("#network-span").css("color", "#000000");
        $("#network-span").siblings().css("color", "#cccccc");
        $("#network-info").siblings().hide();
        $("#network-info").show();
    });
    $("#connections-span").click(function () {
        $("#connections-span").css("color", "#000000");
        $("#connections-span").siblings().css("color", "#cccccc");
        $("#connections-info").siblings().hide();
        $("#connections-info").show();
    });
});