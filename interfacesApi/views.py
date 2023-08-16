from hashlib import new
from pathlib import Path
import mimetypes
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, HttpResponse,JsonResponse
from .azure_messages_hndlr import send_request_messagses
from .azure_file_controller import ALLOWED_EXTENTIONS, upload_file_to_blob, list_blobs, delete_file_blob
import json
from . import models


def index(request):
    return render(request, "interfacesApi/index.html", {})

def file_management(request):
    if request.method == 'GET':
        files = list_blobs()
        # files = str(files)
        list_of_files = {
            'files':files,
        }
        print(list_of_files)
    return render(request, "interfacesApi/file_management.html", list_of_files)

def ecu_info(request):
    return render(request, "interfacesApi/ecu_info.html", {})

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix
        new_file = upload_file_to_blob(file)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "interfacesApi/upload_file.html", {}) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        messages.success(request, f"{file.name} was successfully uploaded")
        return redirect('file_management')

    return render(request, "interfacesApi/upload_file.html", {})

def list_files(request):
    if request.method == 'GET':
        files = list_blobs()
        files = str(files)
        list_of_files = {
            'files':files,
        }
        return JsonResponse(list_of_files)



def get_diag_messages(request):
    print("trigger")
    if request.method == 'POST': 
        print("step in Post")
        diag_messages_input = request.POST.get('diag_service')
        send_request_messagses(diag_messages_input,'Diag')
        print(diag_messages_input)
        response_data = {'message':'Text input received successfully'}
        return HttpResponse(response_data)
    else:
        print("step in error")
        return HttpResponse({'error':'INvalid request.'},status=400)

def delete_files(request):
    if request.method == 'POST':
        print('in')
        file_name_input = request.body
        # Decode bytes to a string
        json_string = file_name_input.decode('utf-8')

        # Convert the JSON string to a dictionary
        data_dict = json.loads(json_string)
        for data in data_dict["file_names"]:
            print(data)
            delete_file_blob(data)
        messages.success(request, f"Delete was successfully")
        return redirect('file_management')
        # file_deleted = delete_file_blob(file_name_input)
        # if file_deleted == True:
        #     return JsonResponse({'Res':'Success delete file'})
        # else:
        #     return JsonResponse({'Res':''})

