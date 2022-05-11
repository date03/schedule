def _trans(s):
    if("[transed]" in s):
        return "".join(s.split(" ")[1:])
    elif("で接続しました" in s):
        return s.split(" ")[0] + " *" + s.split(" ")[7] + "が参加しました"
    elif("left the game" in s):
        return s.split(" ")[0] + " " + s.split(" ")[3] + "が退出しました"
    elif("main WARN Unable to instantiate" in s):
        return "↑↑↑↑↑" + s.split(" ")[0] + "↑↑↑↑↑"
    elif("Starting minecraft server" in s):
        return s.split(" ")[0] + " サーバーが起動しました"
    elif("Stopping server" in s):
        return s.split(" ")[0] + " サーバーが停止しました"
    elif("Async Chat Thread" in s):
        return s.split(" ")[0] + " " + "".join(s.split(" ")[6:])
    else:
        return None


def log(flag=False):
    if(flag):
        path = "./log.txt"
    else:
        path = "module/log.txt"
    with open(path) as f:
        micra_log = [_trans(s) for s in f.readlines()]
    micra_log = [x for x in micra_log if x is not None]
    if(flag):
        with open(path, 'w') as f:
            f.write("[transed] " +
                    "\n[transed] ".join(micra_log).replace("\n\n", "\n"))
    else:
        micra_log.reverse()
        return micra_log[0:min(100, len(micra_log))]


if __name__ == "__main__":
    log(flag=True)
