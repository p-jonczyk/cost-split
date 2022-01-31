

def total_cost(single_plan):
    """Returns total cost of a single plan

    Parameter
    single_plan: single plan from database

    Returns: total cost of a single plan"""
    costs = single_plan.cost_set.all()
    if costs:
        total_cost = 0
        for cost in costs:
            total_cost += cost.cost

        return total_cost
    else:
        return 0


def total_per_person(single_plan):
    """Returns total cost per person

    Parameter
    single_plan: single plan from database

    Returns: total cost per person"""
    costs = single_plan.cost_set.all()

    if costs:
        total_cost = 0
        for cost in costs:
            cost_per_person = round(cost.cost / cost.number_of_members, 2)
            total_cost += cost_per_person
        return total_cost
    else:
        return 0


def paid_cost(single_plan):
    """Count paid cost of a single plan

    Parameter
    single_plan: single plan from database

    Returns: paid costs of a single plan"""
    costs = single_plan.cost_set.all()
    if costs:
        paid_cost = 0
        for cost in costs:
            if cost.cost_status:
                paid_cost += cost.cost

        return paid_cost
    else:
        return 0
