from django.shortcuts import render, redirect, get_object_or_404, Http404, reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import UserProfile
from .forms import ProfileForm, AvatarUploadForm

import uuid
from django.http import JsonResponse
from PIL import Image
import os
import json

def crop_image(current_avatar, file, data, uid):
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10],ext) #随机生成新的图片名
    cropped_avatar = os.path.join(str(uid),'avatar', file_name) #相对路径
    file_path = os.path.join('media', cropped_avatar) # 加 media的路径
    coords = json.loads(data) #获取Ajax发送的裁剪参数data. 先用 json解析
    t_x = int(coords['x'])
    t_y = int(coords['y'])
    t_width = t_x + int(coords['width'])
    t_height = t_y + int(coords['height'])
    t_rotate = coords['rotate']
    img = Image.open(file)
    crop_im = img.crop((t_x,t_y,t_width,t_height)).resize((200,200,), Image.ANTIALIAS).rotate(t_rotate) #裁剪图片
    directory = os.path.dirname(file_path)
    if os.path.exists(directory):
        crop_im.save(file_path)
    else:
        os.makedirs(directory)
        crop_im.save(file_path)

    if not current_avatar == os.path.join('avatar','default.jpg'):
        current_avatar_path = os.path.join('media', str(uid),"avatar", os.path.basename(current_avatar.url))
        os.remove(current_avatar_path)
    return cropped_avatar #返回相对于 media的路径


# Create your views here.
@login_required
def profile(request):
    user = request.user
    return render(request,'myaccount/profile.html', {'user':user})

@login_required
def profile_update(request):
    user = request.user
    try:
        user_profile = get_object_or_404(UserProfile,user=user)
    except Http404:
        user_profile = UserProfile.objects.create(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()
            return redirect(reverse('myaccount:profile'))
    else:
        default_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'org': user_profile.org,
            'telephone': user_profile.telephone,
        }
        form = ProfileForm(default_data)
    return render(request, 'myaccount/profile_update.html',
                  {
                      'form':form,
                      'user':user
                  })

@login_required
def ajax_avatar_upload(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile,user=user)

    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES["avatar_file"] #获取上传图片
            data = request.POST['avatar_data'] #获取ajax返回图片坐标
            if img.size/1024 >700:
                return JsonResponse({'message':"图片尺寸应小于900x1200像素，请重新上传",})

            current_avatar = user_profile.avatar #当前用户的头像
            cropped_avatar = crop_image(current_avatar,img,data,user.id)
            user_profile.avatar = cropped_avatar #修改 cropped 后的头像
            user_profile.save()
            data = {'result':user_profile.avatar.url} # 返回用户头像路径
            return JsonResponse(data)
        else:
            return JsonResponse({"message":"请重新上传，只能上传图片"})

    return redirect(reverse('myaccount:profile'))
