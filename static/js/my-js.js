/**
 * Created by root on 17-3-30.
 */
$(document).ready(function () {
    $("#swap-span").click(function () {
        $("#memory-span").css("color", "#cccccc");
        $("#swap-span").css("color", "#000000");
        $(".memory").hide();
        $(".swap-info").show();
    });
    $("#memory-span").click(function () {
        $("#swap-span").css("color", "#cccccc");
        $("#memory-span").css("color", "#000000");
        $(".swap-info").hide();
        $(".memory").show();
    });
});