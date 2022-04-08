from django.http import JsonResponse
from django.shortcuts import render
import json
from app.fuzzy import calculate
import os, glob
from django.conf import settings


def index(request):
    return render(request, "app/index.html")


def calculate_time(request):
    if request.method == "POST":
        jsonData = json.loads(request.body)

        # print(jsonData)
        loading_time = float(jsonData.get("loading_value", 0))
        packet_loss_rate = float(jsonData.get("packet_loss_rate", 1))
        # time = calculate(loading_time, packet_loss_rate)
        time, img_name = calculate(loading_time, packet_loss_rate)
        # print(loading_time, packet_loss_rate)
        for filename in glob.glob(f"{settings.BASE_DIR}/staticfiles/app/result*"):
            print(os.path.basename(filename))
            if os.path.basename(filename) == f"{img_name}.png":
                continue
            os.remove(filename)
        return JsonResponse({"time": time, "img": img_name})
    return render(request, "app/index.html")
