
def calc_all_burden(arguments, attacks):

    new={}
    # Generate argument atoms
    for arg in arguments:
        list=[]
        r,list = cal_burd(arg,attacks.copy(),list)
        new[arg.name]=list
    return new 

def foundattack(argument, attacks):
    found = False
    for at in attacks:
     if at[1].name == argument.name :
         found = True
    return found

def cal_burd(argument, attacks,list):
    if foundattack(argument,attacks):
        x = 0
        for at in attacks:
            if at[1].name == argument.name : 
                attacks.remove(at)
                result,list = cal_burd(at[0], attacks,list)
                x += result
        list.append((1 + 1/x))
        return  (1 + 1/x),list
    else:
        list.append(1)
        return (1) , list
    

def compare_lexicographically(dict1, dict2):
    name,list1 = dict1
    name2,list2= dict2

    if  name == name2 or list1 == list2: 
        return False 
    if len(list1)<len(list2):
        x = len(list2)-len(list1)
        y = len(list1)-1
        for k in range(x-1):      
            list1.append(list1[y])
    if len(list1)>len(list2):
        x = len(list1)-len(list2)
        y = len(list2)-1
        for k in range(x-1):      
            list2.append(list2[y])

    # Compare each pair of probabilities lexicographically
    for prob1, prob2 in zip(list1, list2):
        if prob1 < prob2:
            return name  # list1 is lexicographically smaller
        if prob1 > prob2:
            return name2  # list1 is lexicographically smaller

def compare(all_burden):
    final={}
    for e,data in all_burden.items():
        final[e]=0
    for e,data in all_burden.items():
        for c,data2 in all_burden.items():
            x = compare_lexicographically((e,data),(c,data2))
            if not False :
                if x == e:
                    if final[e]>= final[c]:
                        final[c]= final[e]+1
                elif x== c:
                     if final[c]>= final[e]:
                        final[e]= final[c]+1

    sorted_dict = sorted(final.items(), key=lambda item: item[1])
    formatted_keys = []
    # Iterate through sorted items
    for i, (key, value) in enumerate(sorted_dict):
        formatted_keys.append(key)
        if i < len(sorted_dict) - 1 and sorted_dict[i+1][1] == value:
            formatted_keys.append(',')
        elif  i < len(sorted_dict) - 1 : formatted_keys.append('>')
        
    s= "Les préférences :"
    for x in formatted_keys:
         s = s + " " + x
    return s




