#!/bin/bash
function client {
    docker run --rm -it -e KOPERNIK_HOST=$KOPERNIK_HOST cli $@
}
nodeid=$(client create 'bob')
client nodes
client node $nodeid
client delete $nodeid
client node $nodeid
