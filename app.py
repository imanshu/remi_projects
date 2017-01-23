import urllib
import urllib.parse
import urllib.request
import json
import os
import requests

from urllib.parse import urlencode

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
def makeWebhookResult(req):
    if req.get("result").get("action") == "welcome":
        card_content = []
        total_brand = []
        total_color = []
        speech = "welcome"
        b = [
          {
            "type": 0,
            "speech": "Greetings, Welcome to the Walmart Digital Shoe Bot!!"
          },
          {
            "title": "Which category you are looking for :",
            "replies": [
              "Men's Shoes",
              "Women's shoes"
            ],
            "type": 2
          }
        ]
    elif req.get("result").get("action") != "showoutagain" and req.get("result").get("action") != "dontshow":
        size = req['result']['parameters']['size']
        gender1 = req['result']['parameters']['gender']
        brand =  req['result']['parameters']['brand']
        color = req['result']['parameters']['color']
        type = req['result']['parameters']['type']
        retailer = 'Walmart'
        action = req['result']['action']
        page_number = 1
        fo = open("foo.txt","w")
        fo.write(str(page_number));
        fo.close()
        gender = ""
        if gender1 == "Men":
            gender = "Men"
        elif gender1 == "Women":
            gender = "Women"
        else:
            gender = ""
        brand_f = ""
        if brand == "any brand":
            brand_f = ""
        elif brand == "":
            brand_f = ""
        else:
            brand_f = urllib.parse.quote_plus(brand)
        color_f = ""
        if color == "any color":
            color_f = ""
        elif color == "":
            color_f = ""
        else:
            color_f = urllib.parse.quote_plus(color)

        category_id = ""
        if gender == "Women" and type == "Atheletic":
            category_id = "95672"
        elif gender == "Women" and type == "Casual":
            category_id = "62107"
        elif gender == "Women" and type == "Formal":
            category_id = "45333"
        elif gender == "Women" and type == "":
            category_id = "3034"
        elif gender == "Men" and type == "Atheletic":
            category_id = "15709"
        elif gender == "Men" and type == "Casual":
            category_id = "24087"
        elif gender == "Men" and type == "Formal":
            category_id = "53120"
        elif gender == "Men" and type == "":
            category_id = "93427"
        else:
            category_id = "93427"

        category = ""
        if gender == "Women" and type == "Atheletic":
            category = "5438_1045804_1045806_1228540"
        elif gender == "Women" and type == "Casual":
            category = "5438_1045804_1045806_1228545"
        elif gender == "Women" and type == "Formal":
            category = "5438_1045804_1045806_1228546"
        elif gender == "Women" and type == "":
            category = "5438_1045804_1045806"
        elif gender == "Men" and type == "Atheletic":
            category = "5438_1045804_1045807_1228548"
        elif gender == "Men" and type == "Casual":
            category = "5438_1045804_1045807_1228552"
        elif gender == "Men" and type == "Formal":
            category = "5438_1045804_1045807_1228553"
        elif gender == "Men" and type == "":
            category = "5438_1045804_1045807"
        else:
            category = "5438_1045804"

        if retailer == "Walmart":
            final_url = "http://api.walmartlabs.com/v1/search?apiKey=ve94zk6wmtmkawhde7kvw9b3&query=shoes&categoryId=" + category + "&facet=on&facet.filter=gender:" + gender +"&facet.filter=color:" + color_f + "&facet.filter=brand:" + brand_f + "&facet.filter=shoe_size:" + "" + "&format=json&start=1&numItems=20"
            data_read = urllib.request.urlopen(final_url).read()
            data_decode = data_read.decode('utf-8')
            json_data = json.loads(data_decode)
            facet_data = json_data['facets']
            brand_index = [i for i,x in enumerate(facet_data) if x['name'] == 'brand'][0]
            total_brand = facet_data[brand_index]['facetValues']
            #brand1 = facet_data[brand_index]['facetValues'][0]['name']
            #brand2 = facet_data[brand_index]['facetValues'][1]['name']
            #brand3 = facet_data[brand_index]['facetValues'][2]['name']
            #addentityvalues(makeentityvalues(total_brand),'brand')
            color_index = [i for i,x in enumerate(facet_data) if x['name'] == 'color'][0]
            total_color = facet_data[color_index]['facetValues']
            #color1 = facet_data[color_index]['facetValues'][0]['name']
            #color2 = facet_data[color_index]['facetValues'][1]['name']
            #color3 = facet_data[color_index]['facetValues'][2]['name']
            #items = json_data['items']
            #addentityvalues(makeentityvalues(total_color),'color')
            total_results = json_data['totalResults']
            if total_results == 0:
                card_content = []
            elif total_results <= 10:
                card_content = makelistwalmart(json_data['items'],num = total_results)
            else:
                card_content = makelistwalmart(json_data['items'],num = 10)
        
        else:
            final_url = "http://svcs.ebay.com/services/search/FindingService/v1?operation-name=findItemsAdvanced&service-version=1.13.0&global-id=EBAY-US&categoryId=" + category_id + "&sortOrde=BestMatch&aspectFilter(0).aspectName=Brand&aspectFilter(0).aspectValueName=" + brand_f + "&aspectFilter(1).aspectName=Color&aspectFilter(1).aspectValueName=" + color + "&aspectFilter(2).aspectName=US+Shoe+Size+%28Men%27s%29&aspectFilter(2).aspectValueName=" + size + "&itemFilter(0).name=ListingType&itemFilter(0).value=FixedPrice&itemFilter(1).name=MinPrice&itemFilter(1).value=0&itemFilter(2).name=MaxPrice&itemFilter(2).value=9999999&itemFilter(3).name=HideDuplicateItems&itemFilter(3).value=true&paginationInput.entriesPerPage=10&paginationInput.pageNumber=1&descriptionSearch=false&security-appname=anshukan-mybot-PRD-a45f0c763-f70377ab&response-data-format=json"
            data_read = urllib.request.urlopen(final_url).read()
            data_decode = data_read.decode('utf-8')
            json_data = json.loads(data_decode)
            card_content = []
            total_results = 0
        speech = "we recommend you to buy " + gender + "!!" + color + "!" + "size" + " size " + brand + "!!!" + type + " please look at image"		
        if gender == "":
            b = {
              "title": "you are looking shoes for :",
              "replies": [
              "Men",
              "Women"
              ],
              "type": 2
            }
        elif type == "":
            b = {
              "title": "please select the category:",
              "replies": [
              "Atheletic",
              "Casual",
              "Formal"
              ],
              "type": 2
            }
        elif total_results == 0 and action == "ebaykeywordsearch":
            b = {
              "title": "no matching result found ,please search again:",
              "replies": [
              ""
              ],
              "type": 2
            }
        elif total_results == 0 and action == "ebaykeywordsearchtype":
            b = {
              "title": "no matching result found for selected type ,please search again:",
              "replies": [
              ""
              ],
              "type": 2
            }
        elif color == "":
            b = {
              "title": "please select the color:",
              "replies": makeentityvalues(total_color,'color'),
              "type": 2
            }
        elif total_results == 0 and action == "ebaykeywordsearch2":
            b = {
              "title": "please select the color:",
              "replies": makeentityvalues(total_color,'color'),
              "type": 2
            }
        elif brand == "":
            b = {
              "title": "please select the brand:",
              "replies": makeentityvalues(total_brand,'brand'),
              "type": 2
            }
        elif total_results == 0 and action == "ebaykeywordsearch3":
            b = {
              "title": "No results found for entered brand ,please try another:",
              "replies": makeentityvalues(total_brand,'brand'),
              "type": 2
            }
        elif size == "":
            b = {
              "title": "please select the size:",
              "replies": [
              "8",
              "9",
              "10"
              ],
              "type": 2
            }
        elif total_results == 0 and action == "ebaykeywordsearch4":
            b = {
              "title": "NO result found for selected size : Please try another size",
              "replies": [
              "8",
              "9",
              "10"
              ],
              "type": 2
            }
        else:
            b = {
              "title": "click on button for more result:",
              "replies": [
              "showmore"
              ],
              "type": 2
            }
        
    elif req.get("result").get("action") == "dontshow":
        size = req['result']['parameters']['size']
        gender1 = req['result']['parameters']['gender']
        brand =  req['result']['parameters']['brand']
        color = req['result']['parameters']['color']
        type = req['result']['parameters']['type']
        shoe = req['result']['parameters']['shoe']
        retailer = 'Walmart'
        #retailer_f = 'Walmart'
        action = req['result']['action']
        #page_number = 1
        #fo = open("foo.txt","w")
        #fo.write(str(page_number));
        #fo.close()
        gender = ""
        if gender1 == "Men":
            gender = "Men"
        elif gender1 == "Women":
            gender = "Women"
        else:
            gender = ""
        brand_f = ""
        if brand == "any brand":
            brand_f = ""
        elif brand == "":
            brand_f = ""
        else:
            brand_f = urllib.parse.quote_plus(brand)
        color_f = ""
        if color == "any color":
            color_f = ""
        elif color == "":
            color_f = ""
        else:
            color_f = urllib.parse.quote_plus(color)

        category_id = ""
        if gender == "Women" and type == "Atheletic":
            category_id = "95672"
        elif gender == "Women" and type == "Casual":
            category_id = "62107"
        elif gender == "Women" and type == "Formal":
            category_id = "45333"
        elif gender == "Women" and type == "":
            category_id = "3034"
        elif gender == "Men" and type == "Atheletic":
            category_id = "15709"
        elif gender == "Men" and type == "Casual":
            category_id = "24087"
        elif gender == "Men" and type == "Formal":
            category_id = "53120"
        elif gender == "Men" and type == "":
            category_id = "93427"
        else:
            category_id = "93427"

        category = ""
        if gender == "Women" and type == "Atheletic":
            category = "5438_1045804_1045806_1228540"
        elif gender == "Women" and type == "Casual":
            category = "5438_1045804_1045806_1228545"
        elif gender == "Women" and type == "Formal":
            category = "5438_1045804_1045806_1228546"
        elif gender == "Women" and type == "":
            category = "5438_1045804_1045806"
        elif gender == "Men" and type == "Atheletic":
            category = "5438_1045804_1045807_1228548"
        elif gender == "Men" and type == "Casual":
            category = "5438_1045804_1045807_1228552"
        elif gender == "Men" and type == "Formal":
            category = "5438_1045804_1045807_1228553"
        elif gender == "Men" and type == "":
            category = "5438_1045804_1045807"
        else:
            category = "5438_1045804"

        if retailer == "Walmart":
            final_url = "http://api.walmartlabs.com/v1/search?apiKey=ve94zk6wmtmkawhde7kvw9b3&query=shoes&categoryId=" + category + "&facet=on&facet.filter=gender:" + gender +"&facet.filter=color:" + color_f + "&facet.filter=brand:" + brand_f + "&facet.filter=shoe_size:" + "" + "&format=json&start=1&numItems=10"
            data_read = urllib.request.urlopen(final_url).read()
            data_decode = data_read.decode('utf-8')
            json_data = json.loads(data_decode)
            facet_data = json_data['facets']
            brand_index = [i for i,x in enumerate(facet_data) if x['name'] == 'brand'][0]
            total_brand = facet_data[brand_index]['facetValues']
            #brand1 = facet_data[brand_index]['facetValues'][0]['name']
            #brand2 = facet_data[brand_index]['facetValues'][1]['name']
            #brand3 = facet_data[brand_index]['facetValues'][2]['name']
            #addentityvalues(makeentityvalues(total_brand),'brand')
            color_index = [i for i,x in enumerate(facet_data) if x['name'] == 'color'][0]
            total_color = facet_data[color_index]['facetValues']
            #color1 = facet_data[color_index]['facetValues'][0]['name']
            #color2 = facet_data[color_index]['facetValues'][1]['name']
            #color3 = facet_data[color_index]['facetValues'][2]['name']
            #items = json_data['items']
            #addentityvalues(makeentityvalues(total_color),'color')
            total_results = json_data['totalResults']
            card_content = []
            total_results = 0
            
        else:
            final_url = "http://svcs.ebay.com/services/search/FindingService/v1?operation-name=findItemsAdvanced&service-version=1.13.0&global-id=EBAY-US&categoryId=" + category_id + "&sortOrde=BestMatch&aspectFilter(0).aspectName=Brand&aspectFilter(0).aspectValueName=" + brand_f + "&aspectFilter(1).aspectName=Color&aspectFilter(1).aspectValueName=" + color + "&aspectFilter(2).aspectName=US+Shoe+Size+%28Men%27s%29&aspectFilter(2).aspectValueName=" + size + "&itemFilter(0).name=ListingType&itemFilter(0).value=FixedPrice&itemFilter(1).name=MinPrice&itemFilter(1).value=0&itemFilter(2).name=MaxPrice&itemFilter(2).value=9999999&itemFilter(3).name=HideDuplicateItems&itemFilter(3).value=true&paginationInput.entriesPerPage=10&paginationInput.pageNumber=1&descriptionSearch=false&security-appname=anshukan-mybot-PRD-a45f0c763-f70377ab&response-data-format=json"
            data_read = urllib.request.urlopen(final_url).read()
            data_decode = data_read.decode('utf-8')
            json_data = json.loads(data_decode)
            card_content = []
            total_results = 0
        speech = "we recommend you to buy " + gender + "!!" + color + "!" + "size" + " size " + brand + "!!!" + type + " please look at image"		
        if shoe == "":
            b = {
              "title": "sorry , I didn't get you ,what you exactly looking for :",
              "replies": [
              "Men's shoes",
              "Women's shoes"
              ],
              "type": 2
            }
        elif gender == "":
            b = {
              "title": "please select the gender:",
              "replies": [
              "Men",
              "Women"
              ],
              "type": 2
            }
        elif type == "":
            b = {
              "title": "unable to recognize, please select from the following category:",
              "replies": [
              "Atheletic",
              "Casual",
              "Formal"
              ],
              "type": 2
            }
        elif total_results == 0 and action == "ebaykeywordsearch":
            b = {
              "title": "no matching result found ,please search again:",
              "replies": [
              ""
              ],
              "type": 2
            }
        elif total_results == 0 and action == "ebaykeywordsearchtype":
            b = {
              "title": "no matching result found for selected type ,please search again:",
              "replies": [
              ""
              ],
              "type": 2
            }
        elif color == "":
            b = {
              "title": "unable to recognize youe choice ,please select from the following color:",
              "replies": makeentityvalues(total_color,'color'),
              "type": 2
            }
        elif total_results == 0 and action == "ebaykeywordsearch2":
            b = {
              "title": "please select the color:",
              "replies": makeentityvalues(total_color,'color'),
              "type": 2
            }
        elif brand == "":
            b = {
              "title": "unable to recognize youe choice ,please select the brand:",
              "replies": makeentityvalues(total_brand,'brand'),
              "type": 2
            }
        elif total_results == 0 and action == "ebaykeywordsearch3":
            b = {
              "title": "No results found for entered brand ,please try another:",
              "replies": makeentityvalues(total_brand,'brand'),
              "type": 2
            }
        elif size == "":
            b = {
              "title": "Sise you entered is not correct or not recogizable ,please select the size:",
              "replies": [
              "8",
              "9",
              "10"
              ],
              "type": 2
            }
        elif total_results == 0 and action == "ebaykeywordsearch4":
            b = {
              "title": "NO result found for selected size : Please try another size",
              "replies": [
              "8",
              "9",
              "10"
              ],
              "type": 2
            }
        else:
            b = {
              "title": "unable to recognize your choice ,let's narrow it down:",
              "replies": [
              "Men's shoes",
              "Women's shoes"
              ],
              "type": 2
            }
    else:
        size = req['result']['parameters']['size']
        gender = req['result']['parameters']['gender']
        brand =  req['result']['parameters']['brand']
        color = req['result']['parameters']['color']
        type = req['result']['parameters']['type']
        retailer = 'Walmart'
        fo = open("foo.txt","r+")
        page_no = fo.read(10);
        fo.close()
        fo = open("foo.txt","w")
        fo.write(str(int(page_no)+1));
        fo.close()
        brand_f = ""
        if brand == "any brand":
            brand_f = ""
        elif brand == "":
            brand_f = ""
        else:
            brand_f = urllib.parse.quote_plus(brand)
        color_f = ""
        if color == "any color":
            color_f = ""
        elif color == "":
            color_f = ""
        else:
            color_f = urllib.parse.quote_plus(color)

        category_id = ""
        if gender == "Women" and type == "Atheletic":
            category_id = "95672"
        elif gender == "Women" and type == "Casual":
            category_id = "62107"
        elif gender == "Women" and type == "Formal":
            category_id = "45333"
        elif gender == "Women" and type == "":
            category_id = "3034"
        elif gender == "Men" and type == "Atheletic":
            category_id = "15709"
        elif gender == "Men" and type == "Casual":
            category_id = "24087"
        elif gender == "Men" and type == "Formal":
            category_id = "53120"
        elif gender == "Men" and type == "":
            category_id = "93427"
        else:
            category_id = "93427"

        category = ""
        if gender == "Women" and type == "Atheletic":
            category = "5438_1045804_1045806_1228540"
        elif gender == "Women" and type == "Casual":
            category = "5438_1045804_1045806_1228545"
        elif gender == "Women" and type == "Formal":
            category = "5438_1045804_1045806_1228546"
        elif gender == "Women" and type == "":
            category = "5438_1045804_1045806"
        elif gender == "Men" and type == "Atheletic":
            category = "5438_1045804_1045807_1228548"
        elif gender == "Men" and type == "Casual":
            category = "5438_1045804_1045807_1228552"
        elif gender == "Men" and type == "Formal":
            category = "5438_1045804_1045807_1228553"
        elif gender == "Men" and type == "":
            category = "5438_1045804_1045807"
        else:
            category = "5438_1045804"
        if retailer == "Walmart":
            final_url = "http://api.walmartlabs.com/v1/search?apiKey=ve94zk6wmtmkawhde7kvw9b3&query=shoes&categoryId=" + category + "&facet=on&facet.filter=gender:" + gender +"&facet.filter=color:" + color_f + "&facet.filter=brand:" + brand_f + "&facet.filter=shoe_size:" + size + "&format=json&start=" + page_no + "1&numItems=10"
            data_read = urllib.request.urlopen(final_url).read()
            data_decode = data_read.decode('utf-8')
            json_data = json.loads(data_decode)
            webpage = "http://c.affil.walmart.com/t/api01?l=http%3A%2F%2Fwww.walmart.com%2Fip%2F3M-Peltor-Junior-Earmuff-Black%2F1498%3Faffp1%3D-ByPQBinFWiAoQigU4w3RKPhjtrlGOUVONY8ulvvMN4%26affilsrc%3Dapi%26veh%3Daff%26wmlspartner%3Dreadonlyapi"
            #items = json_data['items']
            total_results = json_data['totalResults']
            if total_results == 0:
                card_content = []
            elif total_results <= 10:
                card_content = makelistwalmart(json_data['items'],num = total_results)
            else:
                card_content = makelistwalmart(json_data['items'],num = 10)

        else:
            final_url = "http://svcs.ebay.com/services/search/FindingService/v1?operation-name=findItemsAdvanced&service-version=1.13.0&global-id=EBAY-US&categoryId=" + category_id + "&sortOrde=BestMatch&aspectFilter(0).aspectName=Brand&aspectFilter(0).aspectValueName=" + brand_f + "&aspectFilter(1).aspectName=Color&aspectFilter(1).aspectValueName=" + color + "&aspectFilter(2).aspectName=US+Shoe+Size+%28Men%27s%29&aspectFilter(2).aspectValueName=" + size + "&itemFilter(0).name=ListingType&itemFilter(0).value=FixedPrice&itemFilter(1).name=MinPrice&itemFilter(1).value=0&itemFilter(2).name=MaxPrice&itemFilter(2).value=9999999&itemFilter(3).name=HideDuplicateItems&itemFilter(3).value=true&paginationInput.entriesPerPage=10&paginationInput.pageNumber=" + page_no +"&descriptionSearch=false&security-appname=anshukan-mybot-PRD-a45f0c763-f70377ab&response-data-format=json"
            data_read = urllib.request.urlopen(final_url).read()
            data_decode = data_read.decode('utf-8')
            json_data = json.loads(data_decode)
            card_content = []
            total_results = 0
        speech = "we recommend you to buy " + gender + "!!" + color + "!" + "size" + " size " + brand + "!!!" + type + " please look at image"
        if total_results != 0:
            b = {
              "title": "click on the button for more results :",
              "replies": [
              "showmore"
              ],
              "type": 2
            }
        else:
            b = {
              "title": "No more matching Results ,let us try again :",
              "replies": [
              "buy shoes"
              ],
              "type": 2
            }

    addentityvalues(makeentityvalues(total_color,'color'),'color')
    addentityvalues(makeentityvalues(total_brand,'brand'),'brand')
    card_content_final = makefulllist(card_content,b)
    print("Response:")
    print(speech)
    
    return {
        "speech": speech,
        "displayText": speech,
        "messages": card_content_final
        #"data": {},
        #"source": "apiai-onlinestore-shopping"
    }
def addentityvalues(mylist = [], facet = ''):
    global content2
    headers = { 'Content-Type': 'application/json', 'Authorization': 'Bearer cada57da29ca44219abbe79ae9e89dff',}
    for i in range(len(mylist)):
        content2 = []
        data1 = {"value": mylist[i],"synonyms": [mylist[i], mylist[i].title(), mylist[i].upper(), mylist[i].lower()]}
        content2.append(data1)
        requests.post('https://api.api.ai/v1/entities/'+ facet +'/entries?v=20150910', headers=headers, data=str(content2))
    return
def makeentityvalues(mylist = [], facet = ''):
    global content1
    num = len(mylist)
    if num >= 8:
        num = 8
    content1 = []
    for i in range(num):
        content1.append(mylist[i]['name'])
    content1.append("any"+" "+facet)
    return content1
def makelistwalmart(mylist = [], *, num):
    global content
    content = []
    next_no = len(mylist) - num
    for i in range(num):
        a = {
          "title": mylist[i]['name'],
          "subtitle": "$" + str(mylist[i]['salePrice']),
          "imageUrl": mylist[i]['thumbnailImage'],
          "buttons": [
            {
              "text": "buy now",
              "postback": mylist[i]['productUrl']
            },
            {
              "text": "show more like this",
              "postback": "show more"
            }
          ],
          "type": 1
        }
        content.append(a)
    if next_no > 1:
        k = {
          "title": "",
          "subtitle": "",
          "imageUrl": "",
          "buttons": [
            {
              "text": str(next_no) + " " + "more results",
              "postback": "show more"
            }
          ],
          "type": 1
        }
    else:
        k = {
          "title": "",
          "subtitle": "",
          "imageUrl": "",
          "buttons": [
            {
              "text": "no more result",
              "postback": "change "
            }
          ],
          "type": 1
        }
    content.append(k)
    return content
def makefulllist(mylist2 = [],mylist3 = []):
    mylist2.append(mylist3)
    return mylist2
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d")

    app.run(debug=True, port=port, host='0.0.0.0')