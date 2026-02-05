from django.shortcuts import render
import random
import time


def main(request):
    '''main restaurant page.'''
    template_name = "restaurant/main.html"
    return render(request, template_name)


def order(request):
    '''order form page, including a random daily special.'''
    template_name = "restaurant/order.html"

    specials = [["Milk Tea", 6], ["Sweet and Sour Crispy Pork", 13],]
    daily_special = random.choice(specials)

    context = { "special_name": daily_special[0], "special_price": daily_special[1],}
    return render(request, template_name, context)


def confirmation(request):
    '''Process the order form submission and show confirmation.'''
    template_name = "restaurant/confirmation.html"

    ordered_items = []
    total = 0
    context = {}

    if request.POST:

        # I use request.POST.get() instead of request.POST[] to avoid error if a form field is missing or unchecked
        customer_name = request.POST.get("customer_name", "")
        customer_phone = request.POST.get("customer_phone", "")
        customer_email = request.POST.get("customer_email", "")
        instructions = request.POST.get("instructions", "")


     # NEW: required fields check (must have name/phone/email)
        if customer_name == "" or customer_phone == "" or customer_email == "":
            template_name = "restaurant/order.html"
            context = {                     
                "error": "Please enter your name, phone, and email before placing an order.",
                "special_name": request.POST.get("special_name", "Daily Special"),
                "special_price": request.POST.get("special_price", "0"),
            }
            return render(request, template_name, context)


        # 3 fixed menu items，and corresponding prices calculation
        if request.POST.get("item_xlb"):
            ordered_items.append("Xiaolongbao ($10)")
            total = total + 10

        if request.POST.get("item_dongpo"):
            ordered_items.append("Dongpo Pork ($16)")
            total = total + 16

        soup_ordered = False 
        if request.POST.get("item_soup"):
            soup_ordered = True   
            ordered_items.append("Clay Pot Soup ($9)")
            total = total + 9

        # Extra options for soup
        if request.POST.get("extra_tofu"):
            # NEW:block extras unless soup ordered
            if not soup_ordered:
                template_name = "restaurant/order.html" 
                context = {
                    "error": "You can only add soup extras if you order Clay Pot Soup.",
                    "special_name": request.POST.get("special_name", "Daily Special"),
                    "special_price": request.POST.get("special_price", "0"),
                }
                return render(request, template_name, context)
            ordered_items.append(" - Add tofu (+$2)")
            total = total + 2

        if request.POST.get("extra_chicken"):
            # NEW: block extras unless soup ordered
            if not soup_ordered:     
                template_name = "restaurant/order.html"
                context = {   
                    "error": "You can only add soup extras if you order Clay Pot Soup!",
                    "special_name": request.POST.get("special_name", "Daily Special"),
                    "special_price": request.POST.get("special_price", "0"),
                }
                return render(request, template_name, context)
            ordered_items.append(" - Extra chicken (+$1)")
            total = total + 1


        # Daily special，item display randomly
        if request.POST.get("item_special"):
            special_name = request.POST.get("special_name", "Daily Special")
            special_price = request.POST.get("special_price", "0")
            try:
                special_price = int(special_price)
            except:
                special_price = 0

            ordered_items.append(special_name + " ($" + str(special_price) + ")")
            total = total + special_price

        # Ready time: add a random 30 to 60 minutes from now
        minutes = random.randint(30, 60)
        ready_seconds = time.time() + minutes * 60
        ready_time = time.ctime(ready_seconds)

        context = {
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "customer_email": customer_email,
            "instructions": instructions,
            "ordered_items": ordered_items,
            "total": total,
            "ready_time": ready_time,
        }

    return render(request, template_name, context)
