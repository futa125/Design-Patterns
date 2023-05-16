#!/usr/bin/env bash

gcc -shared -fPIC parrot.c -o parrot.so && gcc -shared -fPIC tiger.c -o tiger.so && gcc main.c myfactory.c -ldl && ./a.out parrot Ivan tiger Ana
