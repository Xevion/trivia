// Client Constants
const SCROLL_INTERVAL = 1500;
const AUTOREFRESH_INTERVAL = 3000;

// Client Variables
let AUTOSCROLL = false;
let AUTOREFRESH = false;

// Client Timeouts
let SCROLL_TIMEOUT;
let REFRESH_TIMEOUT;

// Scroll table once.
function ScrollOnce(autoscroll) {
    // If autoscroll has been disabled in between timer, this if statement will prevent it from executing.
    if (AUTOSCROLL)
        $(".team-row:first").appendTo("tbody")

    // Restart autoscroll as needed.
    if (autoscroll && AUTOSCROLL) {
        setTimeout(function () {
            ScrollOnce(true)
        }, SCROLL_INTERVAL)
    }
}

function ToggleAutoscroll() {
    AUTOSCROLL = !AUTOSCROLL;

    if (AUTOSCROLL) {
        $(".js-scroll-row-start").hide();
        $(".js-scroll-row-stop").show();
    } else {
        $(".js-scroll-row-start").show();
        $(".js-scroll-row-stop").hide();
    }
}

function ToggleAutorefresh() {
    AUTOREFRESH = !AUTOREFRESH;

    if (AUTOREFRESH) {
        $(".js-refresh-start").hide();
        $(".js-refresh-stop").show();
    } else {
        $(".js-refresh-start").show();
        $(".js-refresh-stop").hide();
    }
}

// Client Initialization
$().ready(function () {
    // Setup all click functions
    $(".js-scroll-row").on("click", ToggleAutoscroll);
    $(".js-refresh").on("click", ToggleAutorefresh);

    ToggleAutoscroll()
    ToggleAutorefresh()
})