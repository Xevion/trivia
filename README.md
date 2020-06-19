# trivia

A simple locally hosted Flask webapp supporting Trivia competitions.

## Setup

Setup is designed to be as simple as possible with no configuration required. This webapp should only be locally acessible
on at `localhost:5000` unless

```
git clone https://github.com/Xevion/trivia.git
cd trivia
pip install -r requirements.txt
python wsgi.py
```

## Application Design

The webapp has two sides: Client and Server.

### Server

The server provides client code as well as a simple backend API for refreshing the page continuously.

Data fed into the tables is taken from a locally updated file which is continuously watched for updates.

Once an update is seen on the file, said file is read, and if readable, valid JSON is detected, the backend will begin
providing the data to clients as they request it.

Each request is bundled with the last time a request was sent. If no update or change has been seen in the mean time,
the response is empty and nothing occurs (`304 Not Modified`).

If a change in the scores is seen, the response includes a leaderboard.


### Client

The frontend client is a fullscreen table displaying a simple leaderboard.

The leaderboard should scroll up and down in order to display as many teams as needed. Speed should be adjusted
so that text is easily readable even while moving.

A second scrolling option should be available that is not animated and simply moves the top row in the leaderboard to
the bottom of the leaderboard. One row should be made to represent the divider between the top and bottom of the
leaderboard.

| Rank | Team Name  | Total Score | 1 | 2 | 3 | 4 |
|------|------------|-------------|---|---|---|---|
| 1    | Tigers     | 14          | 4 | 2 | 5 | 3 |
| 2    | Orangutans | 9           | 3 | 2 | 0 | 4 |
| 2    | Wolves     | 9           | 0 | 2 | 5 | 2 |
| 4    | Owls       | 7           | 1 | 2 | 0 | 4 |
| 5    | Rats       | 3           | 0 | 2 | 0 | 1 |

- Ranks will be calculated client side.
    - This includes ties for any given rank. Take note that despite there being no Rank 3 in the table, Rank 4 and 5 are
    taken just after 2. Ties should occupy ranks as if no tie system exists at all, although display ties just the same.
- A simple nth place system.
    - First, Second and Third place will be marked with Gold, Silver and Bronze colors. Still considering methods of 
    marking.
        - Simple Image
        - Color Text
        - Color Background

## Ideas

- Method of reading and converting Excel Leaderboards to the proper format.
    - Should be built *failsafe*, given that the file is unreadable or somehow corrupted.
- Build application to support any platform
    - The API should be able to support any kind of platform, from a Windows Application, to an Android App, to a CLI
    implementation.
- A fun CLI implementation of the client.