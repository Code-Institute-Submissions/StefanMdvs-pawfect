from django.shortcuts import render, redirect, reverse

# Create your views here.

def view_bag(request):
    """
    View to render the shopping bag
    """
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """
    A view to add the specified quantity to the bag
    """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['size_of_item'].keys():
                bag[item_id]['size_of_item'][size] += quantity
            else:
                bag[item_id]['size_of_item'][size] = quantity
        else:
            bag[item_id] = {'size_of_item': {size: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity
    
    
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['size_of_item'][size] = quantity
        else:
            del bag[item_id]['size_of_item'][size]
            if not bag[item_id]['size_of_item']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))