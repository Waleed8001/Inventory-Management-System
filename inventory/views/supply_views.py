from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from inventory.models import Item
from inventory.myutils2 import poulateRelatedFields
import json

# def listSupply(request):
#     """
#     Return a list of all supplies in the database.

#     Returns:
#         JsonResponse: A list of all supplies in the database
#     """
#     try:
#         supplies_queryset = Supply.objects.all()

#         supplies_list = json.loads(
#             serialize('json', supplies_queryset)
#         )

#         poulateRelatedFields(supplies_list, 'item', Item)

#         return JsonResponse(
#             {
#                 "message": "Successfully retrieved all Supplies",
#                 "supplies_count": len(supplies_list),
#                 "supplies": supplies_list
#             },
#             status=200
#         )

#     except Exception as e:
#         return JsonResponse(
#             {"error": str(e)}, status=500
#         )


# def retrieveSupply(request, supply_slug):
#     """
#     Retrieve a specific item by slug.

#     Args:
#         request: The request object
#         item_slug: The slug of the item to retrieve

#     Returns:
#         JsonResponse: The item with the matching slug

#     Raises:
#         Item.DoesNotExist: If item with slug doesn't exist
#         Exception: If any other exception occurs
#     """
#     try:
#         supply_retrieved = Supply.objects.get(slug=supply_slug)
#         supply_retrieved = json.loads(
#             serialize('json', [supply_retrieved])
#         )[0]
        
#         return JsonResponse(
#             {
#                 "message": f"Successfully retrieved the supply with slug {supply_slug}",
#                 "Supply": supply_retrieved
#             },
#             status=200
#         )

#     except Supply.DoesNotExist:
#         return JsonResponse(
#             {"error": f"Supply with slug {supply_slug} Doesn't Exists"}, status=404
#         )

#     except Exception as e:
#         return JsonResponse(
#             {"error": str(e)}, status=500
#         )


# @csrf_exempt
# def createSupply(request):
#     """
#     Create an item.

#     Args:
#         request: The request object

#     Returns:
#         JsonResponse: The created item

#     Raises:
#         Exception: If any exception occurs
#     """
#     try:
#         if request.method == 'POST':
#             data = json.loads(request.body)

#             name = data.get('name', '')
#             phone_num = data.get('phone_number', '')
#             email = data.get('email', '')
#             qty_supplied = data.loads('qty_supplied', 0)

#             supplier = Supplier.objects.create(
#                 name=name,
#                 phone_num=phone_num,
#                 email=email,
#             )

#             Stock.objects.create(
#                 item=item, qty_in_stock=qty_in_stock
#             )

#             return JsonResponse(
#                 {
#                     "message": "Successfully added the item",
#                     "item": json.loads(
#                         serialize('json', [item])
#                     )[0]
#                 },
#                 status=201
#             )

#         return JsonResponse(
#             {"error": f"Request method {request.method} not allowed, use POST"}, status=405
#         )

#     except Exception as e:
#         return JsonResponse(
#             {"error": str(e)}, status=500
#         )


# @csrf_exempt
# def updateItem(request, item_slug):
#     """
#     Update an supply by slug.

#     Args:
#         request: The request object
#         supply_slug: The slug of the supply to update

#     Returns:
#         JsonResponse: The updated supply

#     Raises:
#         Supply.DoesNotExist: If supply with slug doesn't exist
#         Exception: If any exception occurs
#     """
#     try:
#         if not request.method in ['PUT', 'PATCH']:
#             return JsonResponse(
#                 {"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405
#             )

#         supply = Supply.objects.get(slug=item_slug)

#         data = json.loads(request.body)

#         if isinstance(data, dict):
#             for field in data:
#                 if field == 'slug':
#                     continue
#                 else:
#                     setattr(supply, field, data[field])

#             supply.save()

#             item_updated = json.loads(
#                 serialize('json', [supply])
#             )[0]

#             return JsonResponse(
#                 {
#                     "message": f"Succesfully updated the supply with slug, {item_slug}.",
#                     "supply": item_updated
#                 },
#                 status=200
#             )

#         else:
#             return JsonResponse(
#                 {"error": "Invalid data format. Please provide a dictionary"}, status=400
#             )

#     except Supply.DoesNotExist:
#         return JsonResponse(
#             {"error": f"Supply with slug {item_slug} Doesn't Exists"}, status=404
#         )

#     except Exception as e:
#         return JsonResponse(
#             {"error": str(e)}, status=500
#         )


# @csrf_exempt
# def deleteSupply(request, item_slug):
#     """
#     Delete an supply by slug.

#     Args:
#         request: The request object
#         supply_slug: The slug of the supply to delete

#     Returns:
#         JsonResponse: The deleted supply

#     Raises:
#         Supply.DoesNotExist: If supply with slug doesn't exist
#         Exception: If any exception occurs
#     """
#     try:
#         if not request.method == 'DELETE':
#             return JsonResponse(
#                 {"error": f"Request method {request.method} not allowed, use DELETE"}, status=405
#             )

#         supply_to_delete = Supply.objects.get(slug=item_slug)
#         supply_to_delete.delete()

#         return JsonResponse(
#             {"message": f"The supply with slug {item_slug} has been deleted succesfully"}, status=204
#         )

#     except Supply.DoesNotExist:
#         return JsonResponse(
#             {"error": f"Supply with slug {item_slug} Doesn't Exists"}, status=404
#         )

#     except Exception as e:
#         return JsonResponse(
#             {"error": str(e)}, status=500
#         )

from inventory.myutils2 import poulateRelatedFields


# Stock views

def listSupply(request):
    """
    Retrieves a list of all stocks in the inventory.

    Returns:
        JsonResponse: A JSON response containing a list of stocks

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        supply_queryset = Supply.objects.all()

        supply_list = json.loads(
            serialize('json', supply_queryset)
        )
        poulateRelatedFields(supply_list, 'item', Item)

        return JsonResponse(
            {
                "message": f"Successfully retrieved all stocks",
                "stocks": supply_list
            },
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieveSupply(request, item_slug):
    """
    Retrieves a stock from the inventory by item-slug.

    Args:
        item-slug (str): The slug of the item whose stock to retrieve

    Returns:
        JsonResponse: A JSON response containing the retrieved stock

    Raises:
        Item.DoesNotExist: If item with slug doesn't exist
        Exception: If any exception occurs
    """
    try:
        item = Supply.objects.get(slug=item_slug)
        item_supply = item.supply

        stock_retrieved = json.loads(
            serialize('json', [item_supply])
        )[0]

        return JsonResponse(
            {
                "message": f"Successfully retrieved the stock of the item with slug {item_slug}",
                "item_stock": stock_retrieved
            },
            status=200
        )

    except Item.DoesNotExist:
        return JsonResponse({"error": f"Item with slug {item_slug} Doesn't Exists"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def updateSupply(request, item_slug):
    """
    Updates a stock from the inventory by item-slug.

    Args:
        item-slug (str): The slug of the item whose stock to update

    Returns:
        JsonResponse: A JSON response containing the updated stock

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        if not request.method in ['PUT','PATCH']:
            return JsonResponse(
                {"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405
            )

        item = Supply.objects.get(slug=item_slug)
        item_stock = item.supply

        data = json.loads(request.body)

        qty_supplied = data.get('qty_supplied', item_stock.qty_supplied)
        item_stock.qty_isupplied = qty_supplied

        item_stock.save()

        stock_updated = json.loads(

            serialize('json', [item_stock])

        )[0]

        return JsonResponse(
            {
                "message": f"Successfully updated the stock of the item with slug {item_slug}",
                "item_stock": stock_updated
            },
            status=200
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=500
        )