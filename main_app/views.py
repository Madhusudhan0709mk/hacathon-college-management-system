import json
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt

from .EmailBackend import EmailBackend
from .models import Attendance, Session, Subject

# Create your views here.


def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("staff_home"))
        else:
            return redirect(reverse("student_home"))
    return render(request, 'main_app/login.html')


def doLogin(request, **kwargs):
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")
    else:
        #Google recaptcha
        captcha_token = request.POST.get('g-recaptcha-response')
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_key = "6LfswtgZAAAAABX9gbLqe-d97qE2g1JP8oUYritJ"
        data = {
            'secret': captcha_key,
            'response': captcha_token
        }
        # Make request
        try:
            captcha_server = requests.post(url=captcha_url, data=data)
            response = json.loads(captcha_server.text)
            if response['success'] == False:
                messages.error(request, 'Invalid Captcha. Try Again')
                return redirect('/')
        except:
            messages.error(request, 'Captcha could not be verified. Try Again')
            return redirect('/')
        
        #Authenticate
        user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("admin_home"))
            elif user.user_type == '2':
                return redirect(reverse("staff_home"))
            else:
                return redirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")



def logout_user(request):
    if request.user != None:
        logout(request)
    return redirect("/")


@csrf_exempt
def get_attendance(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        attendance = Attendance.objects.filter(subject=subject, session=session)
        attendance_list = []
        for attd in attendance:
            data = {
                    "id": attd.id,
                    "attendance_date": str(attd.date),
                    "session": attd.session.id
                    }
            attendance_list.append(data)
        return JsonResponse(json.dumps(attendance_list), safe=False)
    except Exception as e:
        return None


def showFirebaseJS(request):
    data = """
    // Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here, other Firebase libraries
// are not available in the service worker.
importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in
// your app's Firebase config object.
// https://firebase.google.com/docs/web/setup#config-object
firebase.initializeApp({
    apiKey: "AIzaSyBarDWWHTfTMSrtc5Lj3Cdw5dEvjAkFwtM",
    authDomain: "sms-with-django.firebaseapp.com",
    databaseURL: "https://sms-with-django.firebaseio.com",
    projectId: "sms-with-django",
    storageBucket: "sms-with-django.appspot.com",
    messagingSenderId: "945324593139",
    appId: "1:945324593139:web:03fa99a8854bbd38420c86",
    measurementId: "G-2F2RXTL9GT"
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();
messaging.setBackgroundMessageHandler(function (payload) {
    const notification = JSON.parse(payload);
    const notificationOption = {
        body: notification.body,
        icon: notification.icon
    }
    return self.registration.showNotification(payload.notification.title, notificationOption);
});
    """
    return HttpResponse(data, content_type='application/javascript')



def resumeinput(request): 
	return render(request, 'resumeinput.html') 
def gen_resume(request): 
	if request.method == 'POST': 
		name = request.POST.get('name', '') 
		about = request.POST.get('about', '') 
		age = request.POST.get('age', '') 
		email = request.POST.get('email', '') 
		phone = request.POST.get('phone', '') 
		skill1 = request.POST.get('skill1', '') 
		skill2 = request.POST.get('skill2', '') 
		skill3 = request.POST.get('skill3', '') 
		skill4 =request.POST.get('skill4', '') 
		skill5 =request.POST.get('skill5', '') 
		degree1 = request.POST.get('degree1', '') 
		college1 = request.POST.get('college1', '') 
		year1 = request.POST.get('year1', '') 
		degree2 = request.POST.get('degree2', '') 
		college2 = request.POST.get('college2', '') 
		year2 = request.POST.get('year2', '') 
		college3 = request.POST.get('college3', '') 
		year3 = request.POST.get('year3', '') 
		degree3 = request.POST.get('degree3', '') 
		lang1 = request.POST.get('lang1', '') 
		lang2 = request.POST.get('lang2', '') 
		lang3 = request.POST.get('lang3', '')	 
		project1= request.POST.get('project1', '') 
		durat1 = request.POST.get('duration1', '') 
		desc1 = request.POST.get('desc1', '') 
		project2 = request.POST.get('project2', '') 
		durat2 = request.POST.get('duration2', '') 
		desc2 = request.POST.get('desc2', '') 
		company1 = request.POST.get('company1', '') 
		post1 = request.POST.get('post1', '') 
		duration1 = request.POST.get('duration1', '') 
		lin11 = request.POST.get('lin11', '') 
		company2 = request.POST.get('company2', '') 
		post2 = request.POST.get('post2', '') 
		duration2 = request.POST.get('duration2', '') 
		lin21 = request.POST.get('lin21', '') 
		ach1 = request.POST.get('ach1', '') 
		ach2 = request.POST.get('ach2', '') 
		ach3 = request.POST.get('ach3', '') 
		return render(request, 'resume.html', {'name':name, 
											'about':about, 'skill5':skill5, 
											'age':age, 'email':email, 
											'phone':phone, 'skill1':skill1, 
											'skill2':skill2, 'skill3':skill3, 
											'skill4':skill4, 'degree1':degree1, 
											'college1':college1, 'year1':year1, 
											'college3':college3, 'year3':year3, 
											'degree3':degree3, 'lang1':lang1, 
											'lang2':lang2, 'lang3':lang3, 
											'degree2':degree2, 'college2':college2, 
											'year2':year2, 'project1':project1, 
											'durat1':durat1, 'desc1':desc1, 
											'project2':project2, 'durat2':durat2, 
											'desc2':desc2, 'company1':company1, 
											'post1':post1, 'duration1': duration1, 
											'company2':company2, 'post2':post2, 
											'duration2': duration2,'lin11':lin11, 
												'lin21':lin21, 'ach1':ach1, 
												'ach2':ach2,'ach3':ach3 }) 
	
	return render(request, 'resumeinput.html') 
