# Sharktest

Programs for testing Megalodon.

## How It Works

Inspired by Stockfish's Fishtest, this is a server-client system that allows
you to use your CPU and run one of the tests.

## How To Use

Download the client Python file (`client.py`) from any of the tests.

The tests are separated into folders in the main directory.

Python package requirements are in `requirements.txt`.

## Current Tests

### [Movegen][movegen]

This is for testing Megalodon's move generation accuracy.

### [Evalweights][evalweights]

This is for tuning the evaluation accuracy of Megalodon.

[movegen]: https://megalodon-chess.github.io/sharktest/movegen
[evalweights]: https://megalodon-chess.github.io/sharktest/evalweights
