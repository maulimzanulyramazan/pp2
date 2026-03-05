import re  # for regular expressions (text search)
import json  # for JSON output


def parse_receipt(file_path):  # function to parse the receipt file
    with open(file_path, 'r', encoding='utf-8') as f:  # open file in read mode
        data = f.read()  # read all text from the file

    datetime_match = re.search(  # search date and time in the text
        r'Время:\s+(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})',  # pattern: date and time
        data  # text where we search
    )

    date = datetime_match.group(1) if datetime_match else "Unknown"  # get date or "Unknown"
    time = datetime_match.group(2) if datetime_match else "Unknown"  # get time or "Unknown"

    item_pattern = re.findall(  # find all products in the text
        r'\d+\.\s*\n'  # item number like "1."
        r'(.+?)\n'  # product name (one line)
        r'(\d+,\d+)\s*x\s*'  # quantity like "2,000 x"
        r'([\d\s]+,\d{2})\n'  # unit price like "154,00"
        r'([\d\s]+,\d{2})',  # total price like "308,00"
        data  # text where we search
    )

    items = []  # list to store all items

    for match in item_pattern:  # loop through every found item
        name = match[0].strip()  # product name (remove spaces)
        quantity = float(match[1].replace(",", "."))  # change comma to dot, make float
        unit_price = float(match[2].replace(" ", "").replace(",", "."))  # remove spaces, make float
        total_price = float(match[3].replace(" ", "").replace(",", "."))  # remove spaces, make float

        items.append({  # add one item as a dictionary
            "product": name,  # save product name
            "quantity": quantity,  # save quantity
            "unit_price": unit_price,  # save unit price
            "total_price": total_price  # save total price
        })

    total_match = re.search(  # search grand total in the text
        r'ИТОГО:\s*\n([\d\s]+,\d{2})',  # pattern: total number after "ИТОГО:"
        data  # text where we search
    )

    grand_total = (  # set grand total number
        float(total_match.group(1).replace(" ", "").replace(",", "."))  # convert to float
        if total_match else 0.0  # if not found, use 0.0
    )

    if re.search(r'Банковская карта:', data):  # check if payment is by card
        payment_method = "Card"  # set payment method to Card
    else:
        payment_method = "Unknown"  # if not found, set Unknown

    receipt_json = {  # build final result as a dictionary
        "store": "EUROPHARMA",  # store name (fixed)
        "date": date,  # parsed date
        "time": time,  # parsed time
        "items": items,  # list of items
        "summary": {  # summary info
            "total_items": len(items),  # how many items
            "grand_total": grand_total,  # final total
            "payment_method": payment_method  # payment method
        }
    }

    return receipt_json  # return final dictionary


if __name__ == "__main__":  # run only if this file is the main program
    result = parse_receipt("raw.txt")  # parse the file raw.txt
    print(json.dumps(result, indent=4, ensure_ascii=False))  # print JSON красиво