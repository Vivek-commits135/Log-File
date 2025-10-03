function greater(str1, str2) {
    if (str1==str2) return 1;
    split(str1, fields1, " ");
    split(str2, fields2, " ");
    if (fields1[5] > fields2[5]) {
        return 1;
    }
    else if (fields1[5] < fields2[5]) {
        return 0;
    }
    if (mon[fields1[2]] > mon[fields2[2]]) {
        return 1;
    }
    else if (mon[fields1[2]] < mon[fields2[2]]) {
        return 0;
    }
    if (fields1[3] > fields2[3]) {
        return 1;
    }
    else if (fields1[3] < fields2[3]) {
        return 0;
    }
    split(fields1[4], time1, ":");
    split(fields2[4], time2, ":");
    if (time1[1] > time2[1]) {
        return 1;
    }
    else if (time1[1] < time2[1]) {
        return 0;
    }
    if (time1[2] > time2[2]) {
        return 1;
    }
    else if (time1[2] < time2[2]) {
        return 0;
    }
    if (time1[3] >= time2[3]) {
        return 1;
    }
    else {
        return 0;
    }
}
function has(str, arr) {
    for (i in arr) {
        if (arr[i]==str) return 1;
    }
    return 0;
}

BEGIN {
    FS = ",";
    mon["Jan"] = 1;
    mon["Feb"] = 2;
    mon["Mar"] = 3;
    mon["Apr"] = 4;
    mon["May"] = 5;
    mon["Jun"] = 6;
    mon["Jul"] = 7;
    mon["Aug"] = 8;
    mon["Sep"] = 9;
    mon["Oct"] = 10;
    mon["Nov"] = 11;
    mon["Dec"] = 12;
    split(levelstr, levels, ",");
    split(eventstr, events, ",");
    regex="[A-Z][a-z]{2} [A-Z][a-z]{2} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}"
    if (!(from ~ regex) || !(to ~ regex)) exit 1;
}
NR==1{
    print $0;
}
NR>1{
    if (greater($2, from) && greater(to, $2) && has($3, levels) && has($5, events)) {
        print $0;
    }
}
END{}