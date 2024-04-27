def generate_all_rebuts_with_sub_args(arguments):
    """
    Generate all possible rebuts for a given set of arguments, including sub-arguments.

    Parameters:
        arguments (list): List of Argument objects.

    Returns:
        list: List of tuples representing rebuts.
    """
    rebuts = []
    for arg1 in arguments:
        for arg2 in arguments:
            # Check if arg2 is a sub-argument of arg1
            sub = arg2.get_all_sub_arguments()
            arg1_conclusion = arg1.top_rule.conclusion
            arg2_conclusion = arg2.top_rule.conclusion
            # Check if conclusions contradict each other
            arg3 = arg2_conclusion.contrapose()
            if (
                arg1_conclusion.name == arg3.name
                and arg1_conclusion.negated == arg3.negated
            ):
                rebuts.append((arg1, arg2))
            else:
                for su in sub:
                    arg3 = su.top_rule.conclusion.contrapose()
                    if (
                        arg1_conclusion.name == arg3.name
                        and arg1_conclusion.negated == arg3.negated
                    ):
                        rebuts.append((arg1, arg2))
    return rebuts


def generate_all_undercut(arguments):
    """
    Generate all possible undercutts for a given set of arguments, including sub-arguments.

    Parameters:
        arguments (list): List of Argument objects.

    Returns:
        list: List of tuples representing rebuts.
    """
    under = []
    for arg1 in arguments:
        for arg2 in arguments:
            # Check if arg2 is a sub-argument of arg1
            sub = arg2.get_defeasible_rules()
            arg1_conclusion = arg1.top_rule.conclusion
            for su in sub:
                if (
                    arg1_conclusion.name == su.name
                    and arg1_conclusion.negated == su.name.contrapose().negated
                ):
                    under.append((arg1, arg2))
    return under

def check_condition(R1, R2):
    pref = []
    for a in R1:
        for b in R2:
            if a in pref :
                break
            elif a.ruleWeight >= b.ruleWeight:
                pref.append(a)

    if len(pref) == len(R1):
        return True
    else :
        return False

def generate_argument_preference(attacks):
    newattack = []
    for at in attacks:
        # Check if arg2 is a sub-argument of arg1
        sub = at[1].get_all_sub_arguments()
        sub.add(at[1])
        arg1_conclusion = at[0].top_rule.conclusion
        
        for su in sub:
            arg3 = su.top_rule.conclusion.contrapose()
            if (
                arg1_conclusion.name == arg3.name
                and arg1_conclusion.negated == arg3.negated
            ):
                arg1 = at[0].get_defeasible_rules()
                arg2 = su.get_defeasible_rules()
                if not arg1:
                    newattack.append((at[0], at[1])) 
                    break
                elif check_condition(arg1,arg2):
                    newattack.append((at[0], at[1]))
                    break
                    
    return newattack

def generate_all_defeats(all_rebuts,undercuts):
    return all_rebuts+undercuts