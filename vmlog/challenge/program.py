# this is the rolling hash algorithm

# 0: mod, 1: r, 2: h, 3: tmp, 4: flag
program = "M"
program += "+s+>s>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[s<<l>*<s>>l-]<<l-s"  # [0] <- 2**62 - 1 (m), [1] <- 2, [2] <- 1
program += ">l*-s*-s*-s*-s*-s*-s"  # [1] <- r
program += ">l*+++++s*-----s****s"  # [2] <- h
program += ">>l+s"  # p = 4, [4] <- 1
program += "[Ml-s"  # [4] <- 0
program += "<<l"  # load [2]
program += ">"  # p = 3
program += ",["  # input
program += "<<*"  # p = 1, reg = (h + input) * r
program += ">>s"  # [3] <- reg
program += "<<<l"  # reg <- [0]
program += ">>>"  # p = 3
program += "%"  # reg = [3] % reg (<-> tmp % m)
program += "<s"  # [2] <- reg (<->h
program += ">>l<s"  # load [4] ( = 0), then [3] <- 0
program += ">l+s"  # [4] <- 1
program += "<l]"  # load [3] to break
program += ">l]"  # load [4] if end [4] == 0
program += "<<lp"  # print [2]
