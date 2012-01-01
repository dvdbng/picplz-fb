#!/bin/bash

ssh hoyga '(cd /usr/lib/picplz-fb; git pull)'
scp .fb_access_token hoyga:/usr/lib/picplz-fb
