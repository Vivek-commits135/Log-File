BEGIN {
    FS = " ";
    val=1
    tem["1"] = "^\\[[A-Za-z]{3} [A-Za-z]{3} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}\\] \\[(notice|error)\\] jk2_init\\(\\) Found child [0-9]+ in scoreboard slot [0-9]+";
    tem["2"] = "^\\[[A-Za-z]{3} [A-Za-z]{3} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}\\] \\[(notice|error)\\] workerEnv\\.init\\(\\) ok [\/a-zA-Z0-9\.]+";
    tem["3"] = "^\\[[A-Za-z]{3} [A-Za-z]{3} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}\\] \\[(notice|error)\\] mod_jk child workerEnv in error state [0-9]+";
    tem["4"] = "^\\[[A-Za-z]{3} [A-Za-z]{3} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}\\] \\[(notice|error)\\] \\[client [0-9\.]+\\] Directory index forbidden by rule: [a-z/]+";
    tem["5"] = "^\\[[A-Za-z]{3} [A-Za-z]{3} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}\\] \\[(notice|error)\\] jk2_init\\(\\) Can't find child [0-9]+ in scoreboard";
    tem["6"] = "^\\[[A-Za-z]{3} [A-Za-z]{3} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}\\] \\[(notice|error)\\] mod_jk child init [0-9]+ -[0-9]+";
}
val==1{
    for (key in tem) {
        if ($0 ~ tem[key]) {
            next;
        }
    }
    val=0;
}
END {
    if(val==0) exit 1;
    else exit 0;
}