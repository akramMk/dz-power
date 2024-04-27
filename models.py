class Literal:
    def __init__(self, name, negated=False):
        self.name = name
        self.negated = negated

    def __str__(self):
        if self.negated:
            return f"¬{self.name}"
        else:
            return self.name

    def contrapose(self):
        # Return the negation of the literal
        return Literal(self.name, not self.negated)


class Rule:
    rule_counter = 1

    def __init__(
        self, premises, conclusion, defeasible=False, ruleWeight=None,name=""
    ):
        self.premises = [
            premise if isinstance(premise, Literal) else Literal(premise)
            for premise in premises
        ]
        self.conclusion = (
            conclusion if isinstance(conclusion, Literal) else Literal(conclusion)
        )
        self.defeasible = defeasible
        self.name = Literal(f"r{Rule.rule_counter}")
        self.ruleWeight = ruleWeight

        Rule.rule_counter += 1

    def __str__(self):
        premises_str = (
            ", ".join(str(premise) for premise in self.premises)
            if self.premises
            else ""
        )
        conclusion_str = str(self.conclusion)
        rule_symbol = "⇒" if self.defeasible else "⇝"
        ruleWeight = "" if self.ruleWeight == None else self.ruleWeight
        return (
            f"[{self.name}] {premises_str} {rule_symbol} {conclusion_str} {ruleWeight}"
        )

    def contrapose(self):
        all_rules_with_cp = []  # Start with the original rule
        if not self.defeasible and self.premises:
            for j in range(len(self.premises)):
                new_premises = [
                    self.premises[i] if i != j else self.conclusion.contrapose()
                    for i in range(len(self.premises))
                ]
                new_conclusion = self.premises[j].contrapose()
                cp_rule = Rule(new_premises, new_conclusion, self.defeasible)
                all_rules_with_cp.append(cp_rule)  # type: ignore # Add contraposition if applicable
        return all_rules_with_cp

def generate_all_contrapose(rules):
    all_rules_with_cp = []  # Start with an empty list
    for rule in rules:
        all_rules_with_cp.extend(
            rule.contrapose()
        )  # Extend the list with contrapositions of each rule
    return all_rules_with_cp

class Argument:
    argument_counter = 1

    def __init__(self, top_rule, direct_sub_arguments=None, name=""):
        self.top_rule = top_rule
        self.direct_sub_arguments = (
            direct_sub_arguments if direct_sub_arguments is not None else []
        )
        self.name = f"AR{Argument.argument_counter}"
        Argument.argument_counter += 1

    def __str__(self):
        sub_args_str = ", ".join(arg.name for arg in self.direct_sub_arguments)
        rule_symbol = "⇒" if self.top_rule.defeasible else "⇝"
        return f"{self.name}: {sub_args_str} {rule_symbol} {self.top_rule.conclusion} | top Rule : {self.top_rule}"

    def equals(self, other):
        if not isinstance(other, Argument):
            return False
        return self.top_rule == other.top_rule and set(
            self.direct_sub_arguments
        ) == set(other.direct_sub_arguments)

    def get_defeasible_rules(self):
        """
        Get the set of all defeasible rules of the argument.

        Returns:
            set: Set of defeasible rules.
        """
        defeasible_rules = set()
        if self.top_rule.defeasible:
            defeasible_rules.add(self.top_rule)
        for sub_argument in self.direct_sub_arguments:
            defeasible_rules.update(sub_argument.get_defeasible_rules())
        return defeasible_rules

    def get_last_defeasible_rules(self):
        """
        Get the set of last defeasible rules of the argument.

        Returns:
            set: Set of last defeasible rules.
        """
        last_defeasible_rules = set()
        if self.top_rule.defeasible:
            last_defeasible_rules.add(self.top_rule)
        else:  # For strict arguments
            for sub_argument in self.direct_sub_arguments:
                last_defeasible_rules.update(sub_argument.get_last_defeasible_rules())
        return last_defeasible_rules

    def get_all_sub_arguments(self):
        """
        Get the set of all sub-arguments of the argument.

        Returns:
            set: Set of all sub-arguments.
        """
        all_sub_arguments = set(self.direct_sub_arguments)
        for sub_argument in self.direct_sub_arguments:
            all_sub_arguments.update(sub_argument.get_all_sub_arguments())
        return all_sub_arguments



def generate_arguments_from_atomic_rules(rule_list):
    """
    Generates arguments from atomic rules.

    Parameters:
        rule_list (list): The list of rules from which arguments are to be generated.

    Returns:
        list: List of arguments.
    """
    arguments = []
    for rule in rule_list:
        if not rule.premises:  # Check if the rule has no premises
            argument = Argument(rule, [])
            arguments.append(argument)
    return arguments


def generate_combinations(premises, argument_lookup):
    if not premises:
        return [[]]

    premise = premises[0]
    rest = premises[1:]
    current_premise_args = argument_lookup.get((premise.name, premise.negated), [])

    combinations = []
    for arg in current_premise_args:
        for combo in generate_combinations(rest, argument_lookup):
            combinations.append([arg] + combo)
    return combinations


def populate_arguments_with_base_rules2(all_rules, all_arguments):
    argument_lookup = {}
    for arg in all_arguments:
        key = (arg.top_rule.conclusion.name, arg.top_rule.conclusion.negated)
        argument_lookup.setdefault(key, []).append(arg)

    for rule in all_rules:
        if rule.premises:  # La règle a des prémisses
            combinations = generate_combinations(rule.premises, argument_lookup)
            for combo in combinations:
                # Vérifier que chaque combinaison est unique avant d'ajouter un nouvel argument
                new_argument = Argument(rule, combo)
                if not any(
                    new_argument.equals(existing_arg) for existing_arg in all_arguments
                ):
                    all_arguments.append(new_argument)
                    new_key = (
                        new_argument.top_rule.conclusion.name,
                        new_argument.top_rule.conclusion.negated,
                    )
                    argument_lookup.setdefault(new_key, []).append(new_argument)
                else:
                    Argument.argument_counter -= 1
    return all_arguments


def generate_all_arguments(all_rules):
    base_arguments = generate_arguments_from_atomic_rules(all_rules)
    all_arguments = base_arguments.copy()
    new_arguments_added = True

    while new_arguments_added:
        # Enregistrer la taille de la liste avant l'appel de la fonction pour la comparer après
        before = len(all_arguments)

        # Appeler la fonction pour potentiellement ajouter de nouveaux arguments
        all_arguments = populate_arguments_with_base_rules2(all_rules, all_arguments)

        # Vérifier si de nouveaux arguments ont été ajoutés
        after = len(all_arguments)
        new_arguments_added = before != after

    return all_arguments