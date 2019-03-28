from django.contrib.auth.models import User
from django.shortcuts import render
import django
from .models import users
import datetime
from .models import compendium as comped
from .models import coment
from .models import compendium_rate
from .models import coment_rate
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from tagging.models import Tag
from polls.forms import TestForm
from polls.forms import CompendiumForm
import cloudinary
import cloudinary.uploader
import cloudinary.api


cloudinary.config(
    cloud_name="urlcloudinaryurl",
    api_key="462295568945981",
    api_secret="IphFefwdL3nW8IjUzU9YKeyQIJo"
)


def new_era():
    pass


def signin_page(request):
    return render(request, "polls/signin.html", {"user": request.user, "compendium": comped.objects.all(),
                                                 "test": request.GET})


def signup_page(request):
    return render(request, "polls/signup.html", {"user": request.user, "compendium": comped.objects.all()})


def log_out(request):
    logout(request)
    return render(request, "polls/main.html", {"user": request.user, "compendium": comped.objects.all()})


def signup(request):
    for i in User.objects.all():
        if str(i) == request.POST.get('firstname'):
            return render(request, "polls/signup.html", {"error": True})
    user = User.objects.create_user(request.POST.get('firstname'),
                                    request.POST.get('secondname'),
                                    request.POST.get('password'))
    user.is_active = False
    user_extra = users(user=user, blockage=False, Fio="", University="", Faculty="", Speciality="")
    user.save()
    user_extra.save()
    current_site = get_current_site(request)
    mail_subject = 'Activate your blog account.'
    message = render_to_string('polls/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': account_activation_token.make_token(user),
    })
    to_email = request.POST.get('secondname')
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return HttpResponse('Please confirm your email address to complete the registration')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def veiw_compendium(request, compendium_id):
    compendium = comped.objects.filter(id=int(compendium_id))
    return render(request, "polls/compendium.html", {"user": request.user,
                                                     "tags": Tag.objects.usage_for_model(comped, counts=True),
                                                     "coments": coment.objects.filter(compendiums=compendium[0]),
                                                     "compendium": compendium[0],
                                                     "user_extend": users.objects.filter(
                                                         user=User.objects.filter(username=request.user))}
                  )


def add_comment(request):
    coments = coment()
    coments.users = request.user
    coments.containment = request.GET['containment']
    coments.compendiums = comped.objects.filter(id=int(request.GET['compendium']))[0]
    coments.save()
    print('Commentary edded')
    return render(request, "polls/compendium_logged.html", {"username": request.user, "user": request.user})


def veiw_compendium_logged(request, compendium_id):
    compendium = comped.objects.filter(id=int(compendium_id))
    return render(request, "polls/compendium_logged.html", {"user": request.user,
                                                            "tags": Tag.objects.usage_for_model(comped, counts=True),
                                                            "coments": coment.objects.filter(compendiums=compendium[0]),
                                                            "compendium": compendium[0],
                                                            "latest_comment": coment.objects.latest('id'),
                                                            "user_extend": users.objects.filter(
                                                                user=User.objects.filter(username=request.user)[0]),
                                                            })


def change_rate(request):
    com = comped.objects.filter(id=int(request.GET['compendium']))
    if len(compendium_rate.objects.filter(correspondent=request.user)) == 0:
        print('hello' + request.GET['compendium'])

        print('hello' + str(request.GET['rate']))
        com_rate = compendium_rate(compendiums=com[0], correspondent=request.user, rate=int(request.GET['rate']))
        com_rate.save()
        amount = len(compendium_rate.objects.filter(compendiums=com[0]))
        com.update(rating=(com[0].rating * amount + int(request.GET['rate']) / amount + 1))
    else:
        print("already liked")
        print('hello' + request.GET['compendium'])
        print('hello' + str(request.GET['rate']))
        print(len(
            compendium_rate.objects.filter(compendiums=comped.objects.filter(id=int(request.GET['compendium']))[0])))
    return render(request, "polls/compendium.html",
                  {"user_extend": users.objects.filter(user=User.objects.filter(username=request.user)[0]),
                   "tags": Tag.objects.usage_for_model(comped, counts=True),
                   "user": request.user})


def save_like(request):
    com = coment.objects.filter(id=int(request.GET['coment']))
    if len(coment_rate.objects.filter(comentarys=com[0], users=request.user)) == 0:
        print('hello' + request.GET['coment'])

        com_rate = coment_rate(users=request.user, comentarys=com[0], rate=True)
        com_rate.save()
        com.update(likes=(com[0].likes + 1))
    else:
        print("already liked")
    return render(request, "polls/compendium.html",
                  {"user_extend": users.objects.filter(user=User.objects.filter(username=request.user)[0]),
                   "tags": Tag.objects.usage_for_model(comped, counts=True),
                   "user": request.user})


def refresh_comment(request):
    last_comment = coment.objects.filter(id=int(request.GET['latest_comment']))
    latest_comment = coment.objects.latest('id')
    new_comments = coment.objects.all()[last_comment[0].id:latest_comment.id]

    return render(request, "polls/refresh_comments.html",
                  {"user_extend": users.objects.filter(user=User.objects.filter(username=request.user)[0]),
                   "tags": Tag.objects.usage_for_model(comped, counts=True),
                   "user": request.user, "comments": new_comments})


def signin(request):
    user = authenticate(username=request.POST.get('name'), password=request.POST.get('password'))

    if user is not None:
        login(request, user)
        if user.is_active:
            return render(request, "polls/main_logged.html", {"tags": Tag.objects.usage_for_model(comped, counts=True),
                                                              "compendium": comped.objects.all(),
                                                              "user_extend": users.objects.filter(
                                                                  user=User.objects.filter(username=request.user)[0])[
                                                                  0],
                                                              "username": request.user.username, "user": request.user})
        else:
            return render(request, "polls/signin.html", {"error": True})
    else:
        return render(request, "polls/signin.html", {"error": True})


def change_val(request):
    user = User.objects.filter(username=request.user)
    user_extend = users.objects.filter(user=User.objects.filter(username=request.user)[0])
    user_extend.update(Fio=request.GET['value_0'], University=request.GET['value_1'],
                       Faculty=request.GET['value_2'], Speciality=request.GET['value_3'])
    return render(request, "polls/private_office.html", {"username": request.user, "user": request.user,
                                                         "debug": "", "user_extend": user_extend[0],
                                                         "tags": Tag.objects.usage_for_model(comped, counts=True),
                                                         "compendium": comped.objects.filter(users=request.user)})


def change_language(request):
    user = User.objects.filter(username=request.user)
    user_extend = users.objects.filter(user=user[0])
    if user_extend[0].language:
        user_extend.update(language=False)
    else:
        user_extend.update(language=True)
    return render(request, "polls/private_office.html", {"username": request.user, "user": request.user,
                                                         "debug": "", "user_extend": user_extend[0],
                                                         "tags": Tag.objects.usage_for_model(comped, counts=True),
                                                         "compendium": comped.objects.filter(users=request.user)})


def change_theme(request):
    user = User.objects.filter(username=request.user)
    user_extend = users.objects.filter(user=user[0])
    if user_extend[0].style:
        user_extend.update(style=False)
    else:
        user_extend.update(style=True)
    return render(request, "polls/private_office.html", {"username": request.user, "user": request.user,
                                                         "debug": "", "user_extend": user_extend[0],
                                                         "tags": Tag.objects.usage_for_model(comped, counts=True),
                                                         "compendium": comped.objects.filter(users=request.user)})


def send_picture(request):
    print(request.FILES)
    user_extend = users.objects.filter(user=request.user)
    cloudinary.uploader.upload(request.FILES['file'],
                               public_id=request.user.username + str(user_extend[0].images_counter))
    user_extend.update(images_counter=(user_extend[0].images_counter + 1))
    user_extend = users.objects.filter(user=request.user)
    return render(request, "polls/private_office.html", {"username": request.user, "user": request.user,
                                                         "debug": "", "user_extend": user_extend[0],
                                                         "tags": Tag.objects.usage_for_model(comped, counts=True),
                                                         "compendium": comped.objects.filter(users=request.user)})


def delete(request):
    user_extend = users.objects.filter(user=request.user)
    for i in comped.objects.all():
        kill = request.POST.get(i.naming)
        if kill == 'on':
            p = comped.objects.get(naming=i)
            p.delete()
    return render(request, "polls/private_office.html", {"username": request.user, "user": request.user,
                                                         "debug": "", "user_extend": user_extend[0],
                                                         "tags": Tag.objects.usage_for_model(comped, counts=True),
                                                         "compendium": comped.objects.filter(users=request.user)})


# def firstEnter(request):
#     print('')
#
#     tags = Tag.objects.usage_for_model(comped, counts=True)
#     return render(request, "polls/main.html", {"user": request.user, "tags": tags,
#                                                "coments": coment.objects.all(),
#                                                "user_extend": users.objects.filter(
#                                                    user=User.objects.filter(username=request.user)),
#                                                "compendium": comped.objects.all(),
#                                                "test":'HELLO'})
def firstEnter(request):

    return render(request, "polls/new.html", {"form":CompendiumForm})


def add_compendium(request):
    user_extend = users.objects.filter(user=request.user)
    compendium = comped()
    compendium.naming = request.POST.get('naming')
    compendium.containment = request.POST.get('containment')
    compendium.tags = request.POST.get('tags')
    # Tag.objects.update_tags(compendium, request.POST.get('tags'))

    compendium.users = request.user
    compendium.change_date = datetime.datetime.now()
    compendium.save()
    return render(request, "polls/private_office.html", {"username": request.user, "user": request.user,
                                                         "debug": "", "user_extend": user_extend[0],
                                                         "tags": Tag.objects.usage_for_model(comped, counts=True),
                                                         "compendium": comped.objects.filter(users=request.user)})


def save_compendium(request):
    user_extend = users.objects.filter(user=request.user)
    compendium = comped.objects.filter(naming=request.POST.get('naming'))
    compendium.update(containment=request.POST.get('text'), change_date=datetime.datetime.now())
    return render(request, "polls/private_office.html", {"username": request.user, "user": request.user,
                                                         "debug": "", "user_extend": user_extend[0],
                                                         "tags": Tag.objects.usage_for_model(comped, counts=True),
                                                         "compendium": comped.objects.filter(users=request.user)})


def main_logged(request):
    return render(request, "polls/main_logged.html", {"user": request.user,
                                                      "tags": Tag.objects.usage_for_model(comped, counts=True),
                                                      "user_extend": users.objects.filter(
                                                          user=User.objects.filter(username=request.user)[0])[0],
                                                      "compendium": comped.objects.all()})


def private_office(request):
    username = request.user.username
    compendium = comped.objects.filter(users=request.user)
    tags = Tag.objects.usage_for_model(comped, counts=True)
    user_extend = users.objects.filter(user=request.user)
    if len(user_extend) == 0:
        user_extend = users(user=request.user, blockage=False, Fio="", University="", Faculty="", Speciality="")
        user_extend.save()
    user_extend = users.objects.filter(user=request.user)
    return render(request, "polls/private_office.html", {"compendium": compendium,
                                                         "tags": Tag.objects.usage_for_model(comped, counts=True),
                                                         "TestForm": TestForm(), "user_extend": user_extend[0],
                                                         "username": username, "user": request.user})
