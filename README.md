# Coding Mood Server

*It plays horror music when your code breaks, and upbeat music when it works.*

Demo video here: https://youtu.be/1LKTrZamxZk

This is the code for the server used in the Coding Mood solution.

Writing code is a very jarring experience. Regardless of whether or not your code works or everything is broken, the same music plays. We don't let this happen in movies, so why let it happen when we code? My app, "Coding Mood" solves this problem.
*It plays horror music when your code breaks, and upbeat music when it works.*

My solution is a combination of Javascript and Python, with the use of websockets!

## Setup

I would recommend using Poetry to install this package. Installation details here: https://python-poetry.org/docs/

Once you have Poetry installed, run the following command to install this:

```bash
> poetry install
```

## Running the server

```bash
> poetry run python codingmoodserver/app.py
```

Once the server is running, you can fire up the mobile app! Source is here: https://github.com/theartofsoftware/coding-mood-app
