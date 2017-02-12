from bottle import sys, route, run, template, get, post, request
import nltk
import mainLogic
import json

@post('/parsetext')
def do_Parsetext():
        para =  request.forms.get('paragraphs')
        arti = mainLogic.article(para)
        data = arti.main(para,0.5)
        print 'data :',data
        ans ='['
        for k in data:
           ans = ans + json.dumps({k:data[k]}) + ','
        ans = ans+'{}]'
        json_data=ans
        return json_data

try:
    run(host='localhost', port=8015, debug=True)
except KeyboardInterrupt:
    # never reached
    print('exiting...')
