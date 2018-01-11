-module(tut).
-export([double/1]).
-export([fac/1, mult/2]).
-export([convert_length/1]).

fac(1) ->
	1;
fac(N) ->
	N * fac(N - 1).

double(X) ->
	2 * X.

mult(X, Y) ->
	X * Y.

convert_length({centimeter, X}) ->
    {inch, X / 2.54};
convert_length({inch, Y}) ->
    {centimeter, Y * 2.54}.