idu = str(idu)
    boo = False
    c = ''
    with open('n.txt') as x:

        for i in (x):    
            g = [q for q in i.split(', ')]
            
            if g[0] ==idu:
                c = g[0]+', '+g[1]
                boo = True

    if boo == False:
        with open ('n.txt', 'a') as f:
            f.write('\n'+idu+', '+n_p_l)
            print(0)
    else:
        with open ('n.txt', 'r') as f:
            old_data = f.read()
        new_data = old_data.replace(c, ('\n'+idu+', '+n_p_l))
        with open ('n.txt', 'w') as f:
            f.write(new_data)