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
    if (AUTOSCROLL || !autoscroll)
        $(".ui-row:first").appendTo(".js-standings")

    // Restart autoscroll as needed.
    if (autoscroll && AUTOSCROLL) {
        SCROLL_TIMEOUT = setTimeout(function () {
            ScrollOnce(true)
        }, SCROLL_INTERVAL)
    }
}

function ToggleAutoscroll() {
    AUTOSCROLL = !AUTOSCROLL;

    if (AUTOSCROLL) {
        $(".js-scroll-row-start").hide();
        $(".js-scroll-row-stop").show();

        ScrollOnce(true);
    } else {
        $(".js-scroll-row-start").show();
        $(".js-scroll-row-stop").hide();

        clearTimeout(SCROLL_TIMEOUT);
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

        clearTimeout(REFRESH_TIMEOUT);
    }
}

function sortUsingNestedText(parent, childSelector, keySelector) {
    var items = parent.children(childSelector).sort(function (a, b) {
        var vA = parseInt($(keySelector, a).text())
        var vB = parseInt($(keySelector, b).text());
        return (vA < vB) ? 1 : (vA > vB) ? -1 : 0;
    });
    parent.append(items);
}

// Sorts all Teams, rearranging them by Rank
function SortTeams(topTeam = 5) {
    // Sort by total score
    sortUsingNestedText($(".js-standings"), '.ui-row', 'td.js-total-score')

    // Push
    console.log(parseInt($('.js-standings').find('>:first-child').data('row-index')))
    // while ( !== topTeam) {
        // $(".ui-row:first").appendTo("tbody")
    // }
}

// Client Initialization
$().ready(function () {
    // Setup all click functions
    $(".js-scroll-row").on("click", ToggleAutoscroll);
    $(".js-refresh").on("click", ToggleAutorefresh);

    ToggleAutoscroll();
    ToggleAutorefresh();
    SortTeams();
})