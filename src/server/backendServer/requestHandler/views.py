from django.shortcuts import render
from django.http import HttpResponse
from requestHandler.models import User
from .forms import updateForm
import json

fields = ['FirstName',
         'LastName',
         'Email',
         'passWord']
currentUser = None

def recognitionRequestHandler(request):

    # handles the face recognition request, currently not in use now, maybe implemented in the future.

    if request.method == 'GET':
        image = request.FILES
        return HttpResponse(image, content_type="image/jpeg")

        '''
        response = {}
        picture = [2, 3, 4]
        requestedUser = recognitionRequestObject(picture)
        result = recognize(requestedUser)
        response["userId"] = result.userId
        response["song_file_path"] = result.favouriteSongPath
        response["time_processed"] = result.time_recognized
        return HttpResponse(json.dumps(response))
        '''

def requestInfo(request):
    # API that returns all the necessary user infomation for facial recognition
    # security measures might be implemented in the future.

    users = User.objects.all()
    result = {}
    for user in users:
        info = {}
        info['firstName'] = user.FirstName
        info['lastName'] = user.LastName
        info['image'] = user.Image.path
        try:
            info['FavouriteSongName'] = user.FavouriteSong.SongName
            info['FavouriteSongPath'] = user.FavouriteSong.File.path
        except Exception as e:
            info['FavouriteSongName'] = 'NULL'
            info['FavouriteSongPath'] = 'NULL'
        result[user.id] = info
    return HttpResponse(json.dumps(result), content_type="application/json")

def requestLoginInfo(request):
    # API that returns all the necessary user infomation for user login

    users = User.objects.all()
    result = {}
    for user in users:
        info = {}
        info['Email'] = user.Email
        info['passWord'] = user.passWord
        info['id'] = user.id
        result[user.Email] = info
        
    return HttpResponse(json.dumps(result), content_type="application/json")

def requestUpdateUserInfo(request):
    if request.method == 'GET':
        userId = request.GET["userId"]
        user = User.objects.get(id=userId)
        
        initials = {}
        for field in fields:
            initials[field] = user.__dict__[field]
        initials['FavouriteSong'] = user.FavouriteSong
        initials['Image'] = user.Image
        initials['userId'] = user.id
        form = updateForm(initial=initials)
        context = {"form": form}
        return render(request, "requestHandler/updateInfo.html", context)

    elif request.method == 'POST':
        form = updateForm(request.POST, request.FILES)
        if form.is_valid():
            userId = form.cleaned_data['userId']
            user = User.objects.get(id=userId)
            if user is not None:
                for field in fields:
                    user.__dict__[field] = form.cleaned_data[field]
                user.save()
                return HttpResponse("update saved!")
            else:
                return HttpResponse("user not found")
        else:
            return HttpResponse("invalid information")

