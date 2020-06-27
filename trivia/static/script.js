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
function sortTeams(topTeam = 5) {
    // Sort by total score
    sortUsingNestedText($(".js-standings"), '.ui-row', 'td.js-total-score')

    // Push
    console.log(parseInt($('.js-standings').find('>:first-child').data('row-index')))
    // TODO: Fix scrolling functionality
    // while ( !== topTeam) {
    // $(".ui-row:first").appendTo("tbody")
    // }
}

// Returns the current Team ID at the top of the score
function currentTopTeam() {
    return parseInt($('.js-standings').find('>:first-child').data('row-index'));
}

// Sorting comparator for Team JSON objects (post 'total' field calculation)
function ScoreComparator(a, b) {
    if (a.total < b.total)
        return 1;
    if (a.total > b.total)
        return -1;
    return a.id - b.id;
}

// Formally refreshes all data in the table with the server while preserving scroll position.
function refresh() {
    // Remember the team at the top
    let pretop = currentTopTeam()

    // Send AJAX GET request
    // TODO: Implement If-Modified Header
    $.ajax({type: "GET", url: "/api/scores/", dataType: "json"}).done(function (teams) {
        // Calculate Team Score Total
        for (let i = 0; i < teams.length; i++) {
            teams[i].total = 0
            for (let j = 0; j < teams[i].scores.length; j++)
                teams[i].total += teams[i].scores[j]
        }

        teams = teams.sort(ScoreComparator)

        // Calculate Team Rank
        teams[0].rank = "1"
        let prevRank = 1;
        let prevTie = false;
        for (let i = 1; i < teams.length; i++) {
            // If current and previous teams have equal scores, mark them as being tied
            if (teams[i].total === teams[i - 1].total) {
                teams[i].rank = `T${prevRank}`

                // Checks if this is the first tie item, if not it updates the first item in the 'tie sequence'
                if (!prevTie) {
                    prevTie = true;
                    teams[i - 1].rank = `T${teams[i - 1].rank}`
                }
            } else {
                prevTie = false;
                prevRank++;
                teams[i].rank = prevRank.toString()
            }
        }

        // Ensure a space (or char T) exists at the start of each Rank
        for (let i = 0; i < teams.length; i++) {
            teams[i].rank = teams[i].rank.padStart(2)
        }
    })
}


// Client Initialization
$().ready(function () {
    // Setup all click functions
    $(".js-scroll-row").on("click", ToggleAutoscroll);
    $(".js-refresh").on("click", ToggleAutorefresh);

    // ToggleAutoscroll();
    // ToggleAutorefresh();
    // sortTeams();
    refresh()
})