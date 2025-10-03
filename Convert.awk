BEGIN {
    FS=",";
    OFS=",";
    template["E1"] = "jk2_init\\(\\) Found child.*"
    template["E2"] = "workerEnv\\.init\\(\\) ok.*"
    template["E3"] = "mod_jk child workerEnv.*"
    template["E4"] = "\[client [0-9\.]+\] Directory.*"
    template["E5"] = "jk2_init\\(\\) Can't find.*"
    template["E6"] = "mod_jk child init.*"
    mes["E1"] = "jk2_init() Found child <*> in scoreboard slot <*>"
    mes["E2"] = "workerEnv.init() ok <*>"
    mes["E3"] = "mod_jk child workerEnv in error state <*>"
    mes["E4"] = "[client <*>] Directory index forbidden by rule: <*>"
    mes["E5"] = "jk2_init() Can't find child <*> in scoreboard"
    mes["E6"] = "mod_jk child init <*> <*>"
    print "LineId,Time,Level,Content,EventId,EventTemplate";
}

{
    printf "%d,%s,",NR,substr($0, 0, length($0)-1);
    for (key in template) {
        if($3 ~ template[key]) print key, mes[key];
    }
}
END{}