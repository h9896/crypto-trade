"""
python3 start.py -  [ -a auth ] [ -k key ]
                    [ -u userid ] [ -s symbol ]
                    [ -c cost ]    [ -q quantity ]
                    [ -p profit ]
    -h --help       Show usage
    -a --auth       The secret
    -k --key        The api key
    -u --userid     User id
    -s --symbol     Trade symbol
    -c --cost       The cost
    -p --profit     Earn profit(%)
    -q --quantity   Trad amount
    -f --func       Buy/Sell first
    -t --time       Time period
"""
import cex.price
import cex.sign
import strategy.strategy
import sys, getopt

def exit_with_usage(exitcode):
    '''Exit after showing the Usage information.'''
    print(globals()['__doc__'])
    sys.exit(exitcode)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],"ha:k:u:s:c:p:q:f:t:",
        ["help",
        "auth=",
        "key=",
        "userid=",
        "symbol=",
        "cost=",
        "profit=",
        "quantity=",
        "func=",
        "time="])
    except getopt.GetoptError as err:
        print(str(err))
        print("Use -h for usage.")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            exit_with_usage(0)
        elif opt in ("-a", "--auth"):
            auth = arg
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-u", "--userid"):
            userid = arg
        elif opt in ("-c", "--cost"):
            cost = float(arg)
        elif opt in ("-p", "--profit"):
            re = float(float(arg)*0.01+1)
        elif opt in ("-q", "--quantity"):
            amt = float(arg)
        elif opt in ("-s", "--symbol"):
            symbol = arg
        elif opt in ("-t", "--time"):
            t = int(arg)
        elif opt in ("-f", "--func"):
            if arg.upper() == "BUY":
                mt = 1
            elif arg.upper() == "SELL":
                mt = 2
            else:
                mt = 0.5
        else:
            print("option: ", opt)
            print("arg: ", arg)
            assert False, "Program error; unhandled option"
    print("Start")
    syb = cex.price.Price(symbol)
    high = float(syb.ticker()[0]["high"])
    low = float(syb.ticker()[0]["low"])

    authOb = cex.sign.Sign(key, auth, userid)

    while(True):
        if (mt%2) == 1:
            cost = strategy.strategy.Strategy(amt, authOb, cost, re, symbol, t).sell()
            mt+=1
        elif (mt%2) == 0:
            cost = strategy.strategy.Strategy(amt, authOb, cost, re, symbol, t).buy()
            mt+=1
        else:
            break

    


if __name__ == '__main__':
    main()
