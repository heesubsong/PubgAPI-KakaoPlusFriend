from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from app import chicken

server = ['KR', 'AS', 'KAKAO', 'JP', 'NA',
          'EU', 'OC', 'SA', 'SEA', 'RU']
mode = ['Solo', 'Duo', 'Squad']
persons = ['tpp', 'fpp']
server_mode = [
    server[1]+' | '+mode[0], server[1]+' | '+mode[1], server[1]+' | '+mode[2],
    server[2]+' | '+mode[0], server[2]+' | '+mode[1], server[2]+' | '+mode[2],
    server[0]+' | '+mode[0], server[0]+' | '+mode[1], server[0]+' | '+mode[2],
    server[3]+' | '+mode[0], server[3]+' | '+mode[1], server[3]+' | '+mode[2],
    server[4]+' | '+mode[0], server[4]+' | '+mode[1], server[4]+' | '+mode[2],
    server[5]+' | '+mode[0], server[5]+' | '+mode[1], server[5]+' | '+mode[2],
    server[6]+' | '+mode[0], server[6]+' | '+mode[1], server[6]+' | '+mode[2],
    server[7]+' | '+mode[0], server[7]+' | '+mode[1], server[7]+' | '+mode[2],
    server[8]+' | '+mode[0], server[8]+' | '+mode[1], server[8]+' | '+mode[2],
    server[9]+' | '+mode[0], server[9]+' | '+mode[1], server[9]+' | '+mode[2],
]

user_dic = {}

def keyboard(request):
    return JsonResponse({
        "type": "buttons",
        "buttons": ["시작하기", "개발자정보"]
    })


@csrf_exempt
def answer(request):

    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    datacontent = received_json_data['content']
    userkey =  received_json_data['user_key']
    global user_dic
    # global search_info = {}
    
    if datacontent == "시작하기" or datacontent == "다시하기":
        return JsonResponse({
            'message': {
                'text': "==== 서버 선택 ====",
            },
            "keyboard": {
                "type": "buttons",
                "buttons": server
            }
        })
    if datacontent == "개발자정보" :
        return JsonResponse({
            'message': {
                'text': "개발자 : 송희섭\n문의사항 및 버그 : close1021@gmail.com\n",
            },
            "keyboard": {
                "type": "buttons",
                "buttons": ["시작하기"]
            }
        })

    elif datacontent in server:
        return JsonResponse({
            'message': {
                'text': "▶"+datacontent+" 서버 선택 완료 \n ==== 모드 선택 ====",
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [datacontent+' | '+mode[0],
                            datacontent+' | '+mode[1],
                            datacontent+' | '+mode[2]]
            }
        })

    elif datacontent in server_mode:
        server_modes = datacontent.split(' | ')
        user_dic[userkey] = server_modes
        return JsonResponse({
            'message': {
                'text': 
                "▶"+server_modes[0]+" 서버 선택 완료 \n"+
                "▶"+server_modes[1]+" 모드 선택 완료 \n"+  
                "==== 닉네임 입력 ====",
            },
            "keyboard": {
                "type": "text"
            }
        })

    elif type(datacontent) == type("uncheon"):
        user_id = datacontent
        user_dic[userkey] = user_dic[userkey]+[user_id]
        stats = chicken.chicken_api(user_dic[userkey][0],user_dic[userkey][1],user_dic[userkey][2])
        return JsonResponse({
            'message': {
                'text': stats,
            },
            "keyboard": {
                "type": "buttons",
                "buttons": ["다시하기", "개발자정보"]
            }
        })
    else :
        return JsonResponse({
            'message': {
                'text': "오류입니다. 다시시작해주세요",
            },
            "keyboard": {
                "type": "buttons",
                "buttons": ["다시하기"]
            }
        })

