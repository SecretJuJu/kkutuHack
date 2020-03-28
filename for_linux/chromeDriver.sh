#!/bin/bash

str=$(google-chrome --version)

str=$(echo $str | tr " " "\n")

for v in $str:
  do
    echo "[$v]"
  done

echo "your chrome version is : "$v

echo "check your chrome version & download chrome driver!"

firefox "http://chromedriver.storage.googleapis.com/index.html"