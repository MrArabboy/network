from django.http import JsonResponse
from django.shortcuts import render
import json
from app.fuzzy import calculate


def index(request):
    return render(request, "app/index.html")


def calculate_time(request):
    if request.method == "POST":
        jsonData = json.loads(request.body)

        # print(jsonData)
        loading_time = float(jsonData.get("loading_value", 0))
        packet_loss_rate = float(jsonData.get("packet_loss_rate", 1))
        # time = calculate(loading_time, packet_loss_rate)
        time = calculate(loading_time, packet_loss_rate)
        # print(loading_time, packet_loss_rate)
        return JsonResponse({"time": time})
    return render(request, "app/index.html")
