#!/bin/bash

curl https://open.er-api.com/v6/latest/RUB | jq -r ".rates" > lab/currencies.json