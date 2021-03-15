# Movegen

Testing the accuracy of move generation algorithms.

## About

The client program will generate a random chess position
and send that position to Megalodon.

It then compares the internal legal moves (generated with `python-chess`)
and Megalodon's legal moves.

If they do not match, the client will send a message to the server
containing the position.

[Back to documentation home][home]

[home]: https://megalodon-chess.github.io/sharktest/
[file]: https://github.com/megalodon-chess/sharktest/blob/main/movegen/client.py
