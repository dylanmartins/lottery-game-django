# lottery-game-django

## Introduction

This project is a `Lottery system` application which through APIs allows anyone to register and play lottery games. Each day at midnight the lottery event is considered closed and a random lottery winner is selected from all participants for the day.

## Tech Stack

To run this project you will need to have `Python`, `Docker` and `docker-compose` installed in your computer:

- [Docker 20.10.20](<https://www.docker.com/>)
- [docker-compose 1.29.2](<https://docs.docker.com/compose/>)
- [Python 3.9.15](<https://www.python.org/downloads/>)

## Installation and Set Up

1. Execute the command `make run`, this will start to spin up all containers automatically.
> :warning: The containers may raise some errors related to database connection, don't be afraid they will restart and run again automatically :) This happens because postgres takes more time to start accepting requests.
2. After everything is up and running, execute the command `make migrate` when docker is already running, this will apply all django migrations
3. Finally you can access the API documentation in <http://localhost:8000/swagger>

## API Utilization

- This API uses a `JWT Token` to manage the access to the API, to generate this token you first need to create a `user` on the endpoint `/users/register`, this endpoint already returns the `access_token` to be used on the header, like that:
`--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ...'` or through the OpenAPI UI.

- If you forgot your `JWT Token` or it expired you can generate a new one on the endpoint `/users/token`.

- In some endpoints you need to pass your user `UUID`, this is why I created the endpoint `/users/me`, it returns the basic info from your user.

- With the `/lotteries` API you can play/create your lottery games, check all your past games and also check specific ones.

- The `/winning_ballots` API is a read-only endpoint to check all past winning ballots, here you can even filter by `datetime`.

## Tasks

- `get_todays_winning_game`: This task executes automatically every day at midnight, it gets the games from the past day and choses a random winner. Since right now there is always only ONE winner, in case there are multiple games with the same `numbers` this task filters the first game created as the winner.

## Considerations

I think what I'm most proud about this project is that I managed to keep it simple while leaving some stuff ready for improvement (like the multi winner stuff), the project is following a clear pattern and is relatively complete with lints, tests, cleaners and working on docker.

It was a really fun project, with it I could reinforce some things I do automatically in my personal projects that will also help me in my career :)

## Ommited and future work

- As I said there are some product choices that I left it open like multi winner stuff, if we should allow repeated numbers and if we should only soft delete users. But, since this is not the point of the assignment I choose to just left some notes in the code.

- The project is working in Docker but I'm not sure if is kubernetes ready, I'd need more time to implement it.

- It's not fully production ready, there are some safety stuff on settings that I'd try to hash it and put as secrets in the environment instead of in the code, but I'll be honest I don't have enough knowledge to do it alone right now :pensive:

- The project has documentation but I used a django auto generator, and I'm not a big fan of it :laughing: for the time sake it's worth, but based on **my experience in Django** if you want to have a more detailed API spec it's better to do it manually and direct create a collection in `Postman` or make an openapi spec manually using `stoplight`.

## Database model

![plot](./database_model.png)

The `User` model has a `OneToMany` relationship with `LotteryGame`, and since all users can check the `WinningBallot` I thought it would be simpler to not create any relationship and just add two properties (`winning_numbers` and `winning_users`) to fetch this data if necessary.

## Author

* **Dylan Martins Janine de Andrade** - [github](https://github.com/dylanmartins) [linkedin](https://www.linkedin.com/in/dylan-m-j-andrade/)