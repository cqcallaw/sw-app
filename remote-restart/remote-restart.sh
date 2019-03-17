#!/bin/bash

input="machines_list.txt"
while IFS= read -r var
do
	ssh user:password@$var service fooBar restart
done < "$input"
