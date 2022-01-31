from types import NoneType
from django.http import HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CreateNewPlan, CreateNewCost
from .models import Plan, Cost
from costsplit import my_functions

# Create your views here.


def index(response):
    """Home"""

    if response.user.is_authenticated:
        return render(response, 'account/home.html', {})
    else:
        return HttpResponseRedirect('/login')


def single_plan(response, id):
    """Plan information - costs"""

    # if user is logged in
    if response.user.is_authenticated:
        # get single_plan by id
        single_plan = Plan.objects.get(id=id)
        # context for template
        context = {'single_plan': single_plan,
                   'total_cost': my_functions.total_cost(single_plan),
                   'paid_cost': my_functions.paid_cost(single_plan),
                   'total_per_person': my_functions.total_per_person(single_plan)}

        # checkbox of status (functionality)
        if single_plan in response.user.plan.all():
            if response.method == 'POST':
                for cost in single_plan.cost_set.all():
                    # each checkbox with different id
                    if response.POST.get('c' + str(cost.id)) == 'checked':
                        cost.cost_status = True
                    else:
                        cost.cost_status = False
                    cost.save()
                return HttpResponseRedirect(f'/single_plan/{id}')

            return render(response, 'account/single_plan.html', context)
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def create_plan(response):
    """Create plan"""
    # if user is logged in
    if response.user.is_authenticated:

        if response.method == 'POST':
            form = CreateNewPlan(response.POST)
            # chcek form validation
            if form.is_valid():
                # clean data
                t = form.cleaned_data["title"]
                tm = form.cleaned_data["total_members"]
                pinf = form.cleaned_data["plan_info"]
                pd = form.cleaned_data["payment_date"]
                t = Plan(title=t, total_members=tm,
                         payment_date=pd, plan_info=pinf)
                t.save()
                # add new plan to user
                response.user.plan.add(t)

            return HttpResponseRedirect("/")
        else:
            # render new plan view
            form = CreateNewPlan()
        return render(response, 'account/create_plan.html', {'form': form})
    else:
        return HttpResponseRedirect('/login')


def edit_plan(request, id):
    """Edit existing plan"""
    # if user is logged in
    if request.user.is_authenticated:

        single_plan = Plan.objects.get(id=id)
        # upload current values to rendered form (instance)
        form = CreateNewPlan(instance=single_plan)
        if single_plan in request.user.plan.all():
            if request.method == 'POST':
                # upload current values to rendered form (instance)
                form = CreateNewPlan(request.POST, instance=single_plan)
                # data validation
                if form.is_valid():
                    # save changes
                    form.save()

                    return HttpResponseRedirect(f'/single_plan/{id}')
            return render(request, 'account/edit_plan.html',
                          {'form': form, 'single_plan': single_plan})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login')


def delete_plan(request, id):
    """Delete existing plan"""
    # if user is logged in
    if request.user.is_authenticated:

        # get single_plan by id
        single_plan = Plan.objects.get(id=id)
        if single_plan in request.user.plan.all():
            if request.method == 'POST':
                # delete plan
                single_plan.delete()
                return HttpResponseRedirect('/')
            return render(request, 'account/delete_plan.html', {'single_plan': single_plan})
    else:
        return HttpResponseRedirect('/')


def create_cost(request, id):
    """Create cost of plan"""
    # if user is logged in
    if request.user.is_authenticated:

        # get single_cost by id
        single_plan = Plan.objects.get(id=id)
        # if its users plan
        if single_plan in request.user.plan.all():
            if request.method == 'POST':
                # take create cost form
                form = CreateNewCost(request.POST)
                # form validation
                if form.is_valid():
                    cn = form.cleaned_data["cost_name"]
                    c = form.cleaned_data["cost"]
                    nm = form.cleaned_data["number_of_members"]
                    cinf = form.cleaned_data["cost_info"]
                    pd = form.cleaned_data["payment_date"]
                    t = Cost(plan_of_cost=single_plan, cost_name=cn, cost=c, number_of_members=nm,
                             payment_date=pd, cost_info=cinf)
                    # save form data
                    t.save()
                return HttpResponseRedirect(f'/single_plan/{id}')
            else:
                # render create cost form
                form = CreateNewCost()
                context = {'form': form, 'single_plan': single_plan}
                return render(request, 'account/create_cost.html', context)
    else:
        return HttpResponseRedirect('/login')


def edit_cost(request, id):
    """Edit existing cost """
    # if user is logged in
    if request.user.is_authenticated:
        # get cost by id
        single_cost = Cost.objects.get(id=id)
        # get plan by connected to cost plan title
        single_plan = Plan.objects.get(title=single_cost.plan_of_cost)
        # upload current values to rendered form (instance)
        form = CreateNewCost(instance=single_cost)
        if request.method == 'POST':
            # upload current values to rendered form (instance)
            form = CreateNewCost(request.POST, instance=single_cost)
            # validate form
            if form.is_valid():
                form.save()

            return HttpResponseRedirect(f'/single_plan/{single_plan.id}')
        else:
            # render current cost data
            context = {'form': form, 'single_plan': single_plan,
                       'single_cost': single_cost}
            return render(request, 'account/edit_cost.html', context)
    else:
        return HttpResponseRedirect('/login')


def delete_cost(request, id):
    # if user is logged in
    if request.user.is_authenticated:
        # get cost by id
        single_cost = Cost.objects.get(id=id)
        # get plan by connected to cost plan title
        single_plan = Plan.objects.get(title=single_cost.plan_of_cost)
        # if its users plan
        if single_plan in request.user.plan.all():
            if request.method == 'POST':
                # delete cost
                single_cost.delete()
                return HttpResponseRedirect(f'/single_plan/{single_plan.id}')
            context = {'single_plan': single_plan, 'single_cost': single_cost}
            return render(request, 'account/delete_cost.html', context)
    else:
        return HttpResponseRedirect('/')


def generated_link(request, id):
    """Generate link with plan details """
    # get plan by id
    single_plan = Plan.objects.get(id=id)
    # loade context
    context = {'single_plan': single_plan,
               'total_cost': my_functions.total_cost(single_plan),
               'paid_cost': my_functions.paid_cost(single_plan),
               'total_per_person': my_functions.total_per_person(single_plan)}

    return render(request, 'account/generated_link.html', context)
