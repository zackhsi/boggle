Boggle
======

[![Build Status](https://travis-ci.org/zackhsi/boggle.svg?branch=master)](https://travis-ci.org/zackhsi/boggle)
![Docker Pulls](https://img.shields.io/docker/pulls/zackhsi/boggle.svg)

[Boggle](https://en.wikipedia.org/wiki/Boggle) is a word game that is played on
a 4x4 board with 16 letter tiles.

In this particular variant of boggle we are making one modification. Now it is
possible for one or more of the letter tiles to be blank (denoted by `*`).

When a tile is blank, it can be treated as any other letter. Note that in one
game it does not have to be the same character for each word.

For example, if the tiles C, T, and * are adjacent. The words cot, cat, and cut
can all be used.

API
---

The API is documented in [API.yaml](/API.yaml) using [OpenAPI Version
3.0.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md).
It can be viewed on
[swaggerhub](https://app.swaggerhub.com/apis/zackhsi/boggle).

Basic usage:

```sh
# Start Boggle server.
$ ./run

# List games.
$ curl -XGET localhost:8000/games

# Create game.
$ curl -sXPOST localhost:8000/games | jq '.'
{
  "id": "8285fbc8-350d-4bb1-916e-af51128761eb",
  "started_at": null,
  "board": null,
  "created_at": "2018-08-18T04:07:36.935115"
}

# Start game.
$ curl -sXPUT localhost:8000/games/8285fbc8-350d-4bb1-916e-af51128761eb -d '{"started":true}' | jq '.'
{
  "id": "8285fbc8-350d-4bb1-916e-af51128761eb",
  "started_at": "2018-08-18T04:10:26.777045",
  "board": {
    "id": null,
    "letters": "TBOECNHXEUIGTHPU"
  },
  "created_at": "2018-08-18"
}

# Claim a word.
$ curl -w "%{http_code}" -XPOST localhost:8000/games/8285fbc8-350d-4bb1-916e-af51128761eb/words -d '{"word": "PINT"}'
204
```

Development
-----------
Use Docker to develop Boggle.

```sh
# Build Docker image.
$ ./build

# Create testing tables.
$ ENVIRONMENT=testing ./run ./tools/create-tables

# Run tests.
$ ./run ./test

# Run server.
$ ./run

# Run interactive shell.
$ ./run bash
```
