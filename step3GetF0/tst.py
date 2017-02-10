


def main():
    
    lst = [[i for i in range(10)]]
    lst[0] = lst[0] + [125]
    lst[0].append([125])
    print lst[0]
    
main()
