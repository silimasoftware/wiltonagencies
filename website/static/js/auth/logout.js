$(function () {
    t = 6000
    i = 1000
    e = 1
    start = performance.now();
    count_down = setInterval(function () {
        $("#timer").html(Math.floor((t - (performance.now() - start)) / i) + e).fadeIn(e).fadeOut(i)
    }, i);
    setTimeout(function () {
        window.location.href = "http://localhost:5554";
        clearInterval(count_down);
    }, t);
});