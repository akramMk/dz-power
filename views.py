from flask import render_template, request
from models import *
import re

def get_name_from_form(request, prefix):
    tab_name = []
    i = 0
    while f'{prefix}{i}' in request.form:
        rule_name = request.form[f'{prefix}{i}'].strip()
        tab_name.append(rule_name)
        i += 1
    return tab_name


def get_premises_from_form(request, prefix):
    tab_premises = []
    i = 0
    while f'{prefix}{i}' in request.form:
        premises = request.form[f'{prefix}{i}'].split(',')
        tab_premises.append([premise.strip() for premise in premises if premise.strip()])
        i += 1
    return tab_premises

def get_literals_from_premises(tab_premises):
    tab_premises_literal = []
    for premises_list in tab_premises:
        literal_list = []
        for premise in premises_list:
            if premise.startswith('!'):
                literal_list.append(Literal(premise[1:], True))
            else:
                literal_list.append(Literal(premise))
        tab_premises_literal.append(literal_list)
    return tab_premises_literal

def get_conclusions_from_form(request, prefix):
    tab_conclusion = []
    i = 0
    while f'{prefix}{i}' in request.form:
        conclusion = request.form[f'{prefix}{i}'].strip()
        tab_conclusion.append(conclusion)
        i += 1
    return tab_conclusion

def get_literals_from_conclusions(tab_conclusion):
    tab_conclusion_literal = []
    for conclusion in tab_conclusion:
        if conclusion.startswith('!'):
            tab_conclusion_literal.append(Literal(conclusion[1:], True))
        else:
            tab_conclusion_literal.append(Literal(conclusion))
    return tab_conclusion_literal

def get_ruleWeight_from_form(request, prefix):
    tab_ruleWeight = []
    i = 0
    while f'{prefix}{i}' in request.form:
        rule_weight = request.form[f'{prefix}{i}'].strip()
        # Convert the weight to an integer or float as appropriate
        try:
            rule_weight = int(rule_weight)  # or float(rule_weight) if that's more appropriate
        except ValueError:
            # Handle the case where the weight is not a valid integer or float
            rule_weight = None  # Or set a default value
        tab_ruleWeight.append(rule_weight)
        i += 1
    return tab_ruleWeight

def create_rules(tab_premises_literal, tab_conclusion_literal, defeasible,ruleWeight=None):
    rules = []

    for i in range(len(tab_premises_literal)):
        pattern = r"r\d+" #On regarde si apres le r il y a un nombre
        match = re.search(pattern, tab_conclusion_literal[i].name)
        
        if(match) : #Si la conclusion est un regle
            found_rule = find_rule_by_name(tab_conclusion_literal[i].name, rules) #On recupere la regle dans toutes les regles deja crée
            if tab_conclusion_literal[i].negated : 
                print("le literal est bien cree")
                tab_conclusion_literal[i] = Literal(found_rule.name,negated=True)
            else :
                tab_conclusion_literal[i] = Literal(found_rule.name)
        if(defeasible) :
            rules.append(Rule(tab_premises_literal[i], tab_conclusion_literal[i], defeasible,ruleWeight[i]))
        else : 
            rules.append(Rule(tab_premises_literal[i], tab_conclusion_literal[i], defeasible))
    return rules

def find_rule_by_name(rule_name, rules):
    for rule in rules:
        if rule_name == rule.name.name:  # Comparaison avec le nom de la règle
            return rule
    return None 


def submit_knowledge_base_logic(request):
    #Initialise le compteur a 1
    Rule.rule_counter = 1
    
    # Traitement des règles strictes
    tab_premises = get_premises_from_form(request, 'premises')
    tab_premises_literal = get_literals_from_premises(tab_premises)
    tab_conclusion = get_conclusions_from_form(request, 'conclusion')
    tab_conclusion_literal = get_literals_from_conclusions(tab_conclusion)

    rules = create_rules(tab_premises_literal, tab_conclusion_literal, defeasible=False,ruleWeight=None)

    # Traitement des règles défaisables
    d_tab_premises = get_premises_from_form(request, 'dPremises')
    d_tab_premises_literal = get_literals_from_premises(d_tab_premises)
    d_tab_conclusion = get_conclusions_from_form(request, 'dConclusion')
    d_tab_conclusion_literal = get_literals_from_conclusions(d_tab_conclusion)
    d_ruleWeight = get_ruleWeight_from_form(request, 'dRuleWeight')

    d_rules = create_rules(d_tab_premises_literal, d_tab_conclusion_literal, defeasible=True, ruleWeight=d_ruleWeight)
    
    # Rajoute les contraposées
    rule_list = generate_all_contrapose(rules + d_rules)
    
    # Combinez les règles strictes et défaisables
    all_rules = rules + d_rules + rule_list     
    
    Argument.argument_counter=1
    # Crée les arguments 
    all_arguments = generate_all_arguments(all_rules)


    return {'rules': all_rules, 'arguments' : all_arguments }

