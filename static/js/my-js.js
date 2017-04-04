/**
 * Created by root on 17-3-30.
 */
$(document).ready(function () {
    // for memory.html
    $("#swap-span").click(function () {
        $("#memory-span").css("color", "#cccccc");
        $("#swap-span").css("color", "#000000");
        $("#memory").hide();
        $("#swap-info").show();
    });
    $("#memory-span").click(function () {
        $("#swap-span").css("color", "#cccccc");
        $("#memory-span").css("color", "#000000");
        $("#swap-info").hide();
        $("#memory").show();
    });

    // for disks.html
    $("#disk-span").click(function () {
        $("#disk-span").css("color", "#000000");
        $("#part-span").css("color", "#cccccc");
        $("#disk-io-span").css("color", "#cccccc");
        $("#parts").hide();
        $("#disk-io").hide();
        $("#disks").show();
    });
    $("#part-span").click(function () {
        $("#disk-io-span").css("color", "#cccccc");
        $("#disk-span").css("color", "#cccccc");
        $("#part-span").css("color", "#000000");
        $("#disks").hide();
        $("#disk-io").hide();
        $("#parts").show();
    });
    $("#disk-io-span").click(function () {
        $("#part-span").css("color", "#cccccc");
        $("#disk-span").css("color", "#cccccc");
        $("#disk-io-span").css("color", "#000000");
        $("#disks").hide();
        $("#parts").hide();
        $("#disk-io").show();
    });

    // for network.html
    $("#network-span").click(function () {
        $("#connections-span").css("color", "#cccccc");
        $("#network-span").css("color", "#000000");
        $("#connections-info").hide();
        $("#network-info").show();
    });
    $("#connections-span").click(function () {
        $("#network-span").css("color", "#cccccc");
        $("#connections-span").css("color", "#000000");
        $("#network-info").hide();
        $("#connections-info").show();
    });
});