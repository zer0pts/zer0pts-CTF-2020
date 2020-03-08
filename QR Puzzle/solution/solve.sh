#!/bin/sh
tac ../distfiles/key > key.reversed
../distfiles/chall ../distfiles/encrypted.qr key.reversed code.qr
