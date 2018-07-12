import pyrebase
from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth

# Create your views here.
# from rest_framework.templatetags.rest_framework import items
from django.utils.safestring import mark_safe

from mainapp.forms import SchoolModelForm, StudentForm, ParentForm, StaffForm, MyStyleForm
from django.views.generic.base import View
from mainapp.forms import StudentForm, ParentForm, StaffForm
from mainapp.models import School, Course

config = {
    'apiKey': "AIzaSyCrAG2_pI8A00gIAPBniRLqv7Kym2d97f0",
    'authDomain': "fir-project-8cea6.firebaseapp.com",
    'databaseURL': "https://fir-project-8cea6.firebaseio.com",
    'projectId': "fir-project-8cea6",
    'storageBucket': "fir-project-8cea6.appspot.com",
    'messagingSenderId': "609798741798"

}
firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
db = firebase.database()
storage = firebase.storage()

userdata = db.child("Users").get().val()
schooldata=db.child("Schools").get().val()


def sign(request):
    if request.method == "GET":
        return render(request, "source/login.html")
    else:
        email = request.POST.get("email")
        passw = request.POST.get("pass")
        try:
            user = authe.sign_in_with_email_and_password(email, passw)
            uid = user['localId']
            print(uid)
            adminid_list = (list(db.child('Users').child('Admin').shallow().get().val()))
            schooladminid_list = (list(db.child('Users').child('SchoolAdmin').shallow().get().val()))
            studentid_list = (list(db.child('Users').child('Student').shallow().get().val()))
            parentid_list = (list(db.child('Users').child('Parent').shallow().get().val()))
            teacher_list = (list(db.child('Users').child('teacher').shallow().get().val()))
            print(teacher_list)

            if uid in adminid_list:
                # print(user['idToken'])
                session_id = user['idToken']
                request.session['uid'] = str(session_id)
                print(session_id)
                print(request.session['uid'])
                return redirect("companyadmin")
            elif uid in schooladminid_list:
                return redirect("schooladmin")
            elif uid in teacher_list:
                return redirect("teacher")
            elif uid in studentid_list:
                return redirect("student")
            elif uid in parentid_list:
                return redirect("parent")
            else:
                message = "You are not authoriized"
                return render(request, "source/login.html", {"messg": message})
        except:
            pass
            # message = "Invalid Credentials"
            # print(message)
            # return render(request, "source/login.html", {"messg": message})


companyitems = ['Schools']
schoolitems = ['User', 'Courses' ]


def logout(request):
    user_session = authe.current_user
    authe.logout(user_session)
    return sign(request)


def forgotpass(request):
    user = authe.current_user
    authe.send_password_reset_email(user["email"])

    return HttpResponse("account is reset")


def verifyemail(request):
    user = authe.current_user
    print(user)
    authe.send_email_verification(user['idToken'])

    return HttpResponse("Helloo")


# def schoolform(request):
#     form = SchoolModelForm()
#
#     if request.method == 'POST':
#         request.POST._mutable = True
#         r = request.POST
#         print(r)
#         try:
#             if form.is_valid:
#                 form = SchoolModelForm(request.POST)
#                 del r['csrfmiddlewaretoken']
#                 print(r)
#                 db.child("Schools").push(r)
#                 return render(request, 'source/companyadmin.html')
#         except RuntimeError:
#             pass
#
#     return render(request, "source/form.html", {'form': form})



def getusernamelist(which):
    try:
        data = db.child("Users").get().val()
        print(data)
        idlist = list(data[which].keys())
        print(idlist)
        student_namelist = []
        print(student_namelist)
        for i in idlist:
            student_namelist.append(data[which][i]['name'])
        return zip(idlist, student_namelist)
    except:
        pass


def userform(request, formtype, id = None):
    all_list = getusernamelist(formtype)
    print(all_list)
    gradelist = getnameidlist("Grade", "title")
    if formtype == 'teacher':
        form = StaffForm()
        category = "teacher"
    elif formtype == 'Student':
        form = StudentForm()
        category = "Student"
    elif formtype == 'Parent':
        form = ParentForm()
        category = "Parent"

    if id:
        try:
            forminstance = db.child("Users").child(formtype).child(id).get().val()
            if formtype == "Student":
                form = StudentForm(forminstance)
            elif formtype == "Parent":
                form = ParentForm(forminstance)
            elif formtype == "teacher":
                form = StaffForm(forminstance)

        except:
            isupdate = 0
            return HttpResponse("id not valid")  # for adding new data into forms

    if request.method == 'POST':
        print(request.POST)
        request.POST._mutable = True
        email = request.POST.get("email")
        passw = request.POST.get("password")
        r = request.POST
        print(r)


        try:
            if form.is_valid:
                del r['csrfmiddlewaretoken']
                print(r)
                user = authe.create_user_with_email_and_password(email, passw)
                uid = user['localId']
                db.child("Users").child(category).child(uid).set(r)
                db.child("Grade").child(r["grade"]).child("Student").update({uid: "true"})
                return redirect('/mainapp/source/schooladmin/')
        except:
            message = "Unable to create account. Please try again"
            return render(request, "source/schooladmin.html", {"messg": message})

    args = {'form': form, 'items': schoolitems, 'formtype': formtype, 'grade': gradelist, 'all_list':all_list}
    return render(request, "source/form.html", args)


def getnameidlist(which, suitablename):
    try:
        mydata = db.child(which).get().val()
        idslist = list(mydata.keys())
        nameslist = []
        for i in idslist:
            nameslist.append(mydata[i][suitablename])
        # print(nameslist)
        return zip(idslist, nameslist)
    except:
        pass


def tabquiz(request):
    quizlist = getnameidlist("Quiz", "name")
    print(quizlist)
    return render(request, "source/tabquiz.html", {'quizlist': quizlist})


def getform(formtype):
    if formtype == 'Schools':
        modelform = School
        comb_list = []

    elif formtype == 'Courses':
        modelform = Course
        # comb_list = getnameidlist("Programs", "title")

    return (modelform)


def allform(request, formtype, id=None):
    all_list = getnameidlist(formtype, "title")
    gradelist = getnameidlist("Grade", "title")

    class AllForm(forms.ModelForm):
        class Meta:
            model = getform(formtype)
            fields = '__all__'

    if id:
        try:
            forminstance = db.child(formtype).child(id).get().val()
            form = AllForm(forminstance)

        except:
            isupdate = 0
            return HttpResponse("id not valid")  # for adding new data into forms
    else:
        form = AllForm()

    if request.method == 'POST':
        form = AllForm(request.POST)
        request.POST._mutable = True
        r = request.POST
        del r['csrfmiddlewaretoken']

        if form.is_valid:

            # update if request.post has id
            if id:
                db.child(formtype).child(id).update(r)
            else:
                # insert if request.post doesnt have id
                cid = db.child(formtype).push(r)
                courseid = cid["name"]
                try: # For pushing only courseid in grade node
                    db.child("Grade").child(r["grade"]).child("Courses").update({courseid: "true"})
                    db.child("Courses").child(courseid).child("Grade").update({r["grade"]: "true"})
                    return redirect("/mainapp/allform/Courses/")
                except RuntimeError:
                    pass

    if formtype == 'Schools':
        items = companyitems
    else:
        items = schoolitems

    args = {'form': form, 'items': items, 'formtype': formtype, 'all_list': all_list, 'grade':gradelist}
    return render(request, 'source/form.html', args)


def companyadmin(request):
    x = authe.current_user
    # print(x['localId'])
    return render(request, 'source/companyadmin.html', {'items': companyitems})


def schooladmin(request):
    x = authe.current_user
    # print(x['localId'])
    return render(request, 'source/schooladmin.html', {'items': schoolitems})


def studentview(request):
    x = authe.current_user
    # print(x['localId'])
    print(x)
    return render(request, 'source/student.html')


def parent(request):
    x = authe.current_user
    # print(x['localId'])
    return render(request, 'source/parent.html')



def sidebarnav(request):
    return render(request, 'source/sidenavbar.html')



def editprofile(request):
    userinfo = authe.current_user
    uid = userinfo['localId']

    # try:
    #     forminstance = db.child("Users").child("SchoolAdmin").child(uid).get().val()
    #     print(uid)
    #     print(forminstance)
    #     form = StudentForm(forminstance)
    # except RuntimeError:
    #     pass

    try:
        forminstance = db.child("Users").child("Staff").child(uid).get().val()
        print(forminstance)
        form = StaffForm(forminstance)
    except RuntimeError:
        pass

    try:
        forminstance = db.child("Users").child("Student").child(uid).get().val()
        print(uid)
        print(forminstance)
        form = StudentForm(forminstance)
    except RuntimeError:
        pass

    try:
        forminstance = db.child("Users").child("Parent").child(uid).get().val()
        print(forminstance)
        form = ParentForm(forminstance)
    except RuntimeError:
        pass

    return render(request, "source/edit.html", {'form': form})


# Tab Quiz


def takequiz(request):
    return render(request, "source/takequiz.html")


def quizlist(request):
    return render(request, "source/quizlist.html")


def coursequiz(request):
    courselist = getnameidlist("Courses", "title")
    return render(request, "source/coursequiz.html", {'courselist': courselist})


def quizforfun(request):
    return render(request, "source/quizforfun.html")


# for grade
def grade(request):
    gradelist = getnameidlist("Grade", "title")
    print(gradelist)
    if request.method == 'POST':
        request.POST._mutable = True
        r = request.POST
        del r['csrfmiddlewaretoken']
        db.child("Grade").push(r)
        return redirect("/mainapp/grade/")
    args = {'items': schoolitems, 'grade': gradelist}
    return render(request, "source/grade.html", args)


# For Assigning teacher to courses

def assign(request):
    teacher_list = getusernamelist("teacher")
    course_list = getnameidlist("Courses", "title")
    args = {'course_list': course_list, 'teacher_list': teacher_list, 'items':schoolitems}
    if request.method == 'POST':
        request.POST._mutable = True
        r = request.POST
        del r['csrfmiddlewaretoken']
        db.child("Users").child("teacher").child(r["teacher"]).child("Courses").update({r["course"]:"true"})
        print(r["teacher"])
        db.child("Courses").child(r["course"]).child("teacher").update({r["teacher"]:"true"})
        return redirect("schooladmin")

    return render(request, "source/assigncourse.html", args)


def getrelation(which,whichid,node,suitablename):
    try:
        data = db.child(which).child(whichid).child(node).get().val()
        idlist=list(data)
        # print(idlist)
        namelist=[]
        for i in idlist:
            namelist.append(db.child(node).child(i).child(suitablename).get().val())
        # print(namelist)
        return (zip(idlist,namelist))
    except:
        pass
#for teacher-course
def teacher_course(teacherid):
    try:
        data=db.child('Users').child('Teacher').child(teacherid).child('Courses').get().val()
        idlist=list(data)
        namelist=[]
        for i in idlist:
            namelist.append(db.child('Courses').child(i).child('title').get().val())
        return (zip(idlist, namelist))
    except:
        pass



def viewcourse(request,id = None):
    getcid_items = getrelation("Grade", id, "Courses")
    title_list = []
    try:
        for i in getcid_items:
            title_list.append(db.child("Courses").child(i).child("title").get().val())
    except:
        pass

    return render(request, "source/viewcourse.html", {'getcid_items':title_list})


#views for teacher
class TeacherView(View):

    initial = {'key': 'value'}
    template_name = 'teacher/teacherhome.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    # return render(request, self.template_name, {'form': form})
# def students(request):
#     std_name_idlist=getusernamelist("Student")
#     arg={'stdlist':std_name_idlist}
#     return render(request,'teacher/students.html',arg)
def courses(request):
    coursedetail = getnameidlist("Courses", "title")

    if request.method=='POST':
        request.POST._mutable = True
        r=request.POST
        del r['csrfmiddlewaretoken']
        db.child("Courses").push(r)

        return redirect('/mainapp/teacher/courses/')
        # return HttpResponse('<script>alert("thanks");</script>')
    return render(request,'teacher/courses.html',{'courses':coursedetail})

def topic(request):
    topicdetail = getnameidlist("Topics", "title")
    coursedetail = getnameidlist("Courses", "title")
    if request.method=='POST':
        request.POST._mutable = True
        r=request.POST
        del r['csrfmiddlewaretoken']
        cid=r['course']
        topicid=db.child("Topics").push(r)
        tid=topicid['name']
        db.child('Topics').child(tid).child('Courses').update({cid:'true'})
        db.child("Courses").child(cid).child('Topics').update({tid:'true'})
        return redirect('/mainapp/teacher/topics/')
        # return HttpResponse('<script>alert("thanks");</script>')
    return render(request,'teacher/topic.html',{'topics':topicdetail,'courses':coursedetail})


def quizcreate(request):
    coursedetail = getnameidlist("Courses", "title")
    topicdetail = getnameidlist("Topics", "title")
    if request.method=='POST':
        request.POST._mutable = True
        r=request.POST
        del r['csrfmiddlewaretoken']
        x=db.child('Quiz').push(r)
        print(x)
        quizid=x['name']
        # db.child("Courses").child(r['course']).child('quiz').update({quizid:'true'})
        # db.child("Courses").child(r['topic']).child('quiz').update({quizid:'true'})
        db.child("Topics").child(r['topic']).child('Quiz').update({quizid:'true'})
        return redirect('question',quizid=quizid)
    return render(request,'teacher/quizcreate.html',{'courses':coursedetail,'topics':topicdetail})

def question(request,quizid):
    questionlist=getrelation('Quiz',quizid, 'Questions', 'question')
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        request.POST._mutable = True
        r=request.POST
        del r['csrfmiddlewaretoken']
        # if questionid then update
        try:
            qid=r['questionid']
            del r['questionid']
            db.child('Questions').child(qid).update(r)
            return HttpResponse(qid)
        except:#creating new question#qid=questionid
            z=db.child('Questions').push(r)
            qid=z['name']
            #reverse relation for quiz and question
            db.child('Questions').child(qid).child('Quiz').update({quizid: 'true'})
            db.child('Quiz').child(quizid).child('Questions').update({qid: 'true'})
        return HttpResponse(qid)
    return render(request, 'teacher/question.html',{'quizid':quizid,'questionlist':questionlist})

def delete(request,quizid,deleteid):
    if request.method == "GET" and request.is_ajax():
        db.child('Questions').child(deleteid).remove()
        db.child('Quiz').child(quizid).child('Questions').child(deleteid).remove()
        return HttpResponse("Question deleted succesfully")
def questiondetail(request,questionid):
    if request.method == "GET" and request.is_ajax():
        detail=db.child('Questions').child(questionid).get().val()
        print(detail)
        return JsonResponse(detail)



def classes(request):
    return render(request,'teacher/classes.html')

def students(request):
    return HttpResponse("HELLO")

