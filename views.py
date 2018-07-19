
import re

import pyrebase
from django import forms
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import  messages
from mainapp.forms import EditSchoolAdminForm, \
    EditStaffForm, EditStudentForm, EditParentForm
from mainapp.forms import StudentForm, ParentForm, StaffForm
from mainapp.models import School, Course, User, SchoolAdmin

config = {
    'apiKey': "AIzaSyCkskZ8L8IYap9ss_TvYlJfwYh-tsL5sVg",
    'authDomain': "fs-learnclass.firebaseapp.com",
    'databaseURL': "https://fs-learnclass.firebaseio.com",
    'projectId': "fs-learnclass",
    'storageBucket': "fs-learnclass.appspot.com",
    'messagingSenderId': "495916606300"
}
firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def gettoken():
    print("hello")
    user = authe.current_user
    try:
        token = user['idToken']
        return token
    except:
        pass



def sign(request):
    if request.method == "GET":
        return render(request, "source/login.html")
    else:
        print("Hello")
        email = request.POST.get("email")
        passw = request.POST.get("pass")
        try:
            user = authe.sign_in_with_email_and_password(email, passw)
            uid = user['localId']
            print(uid)
            token = user['idToken']
            adminid_list = db.child('Users').child('Admin').shallow().get(token).val()
            schooladminid_list = db.child('Users').child('SchoolAdmin').shallow().get(token).val()
            studentid_list = db.child('Users').child('Student').shallow().get(token).val()
            parentid_list = db.child('Users').child('Parent').shallow().get(token).val()
            teacher_list = db.child('Users').child('Teacher').shallow().get(token).val()

            if uid in list(adminid_list):
                return redirect("companyadmin")
            elif uid in list(schooladminid_list):
                return redirect("schooladmin")
            elif uid in list(teacher_list):
                return redirect("teacher")
            elif uid in list(studentid_list):
                return redirect('student', uid=uid)
            elif uid in list(parentid_list):
                return redirect("parent")
            else:
                message = "You are not authoriized"
                return render(request, "source/login.html", {"messg": message})
        except:

            messages.warning(request, 'Invalid Credential!')
            return render(request, "source/login.html")


companyitems = ['Schools', 'SchoolAdmin', 'questions']
schoolitems = ['User', 'Courses']


def logout(request):
    user = authe.current_user
    # firebase.auth.signOut()
    del user['idToken']
    return sign(request)


def forgotpass(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        try:
            authe.send_password_reset_email(email)
            messages.success(request, '<h4 ">Instruction Sent ! </h4> '
                                      ' Password reset link have been sent to '
                                      '<b>' + email + '</b>'
                                        '<br>Please check it!' , extra_tags='safe')

        except:
            messages.warning(request, 'Invalid Email!')

    return render(request, "source/forgot.html")


def changepass(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        # user = authe.current_user
        try:
            authe.send_password_reset_email(email)
            messages.success(request, '<h4 ">Instruction Sent ! </h4> '
                                      ' Password reset link have been sent to '
                                      '<b>' + email + '</b>'
                                        '<br>Please check it!' , extra_tags='safe')

        except:
            messages.warning(request, 'Invalid Email!')

    return render(request, "source/changepass.html")


def verifyemail(request):
    user = authe.current_user
    print(user)
    authe.send_email_verification(user['idToken'])

    return HttpResponse("Helloo")


def getusernamelist(which, token):
    try:
        data = db.child("Users").get(token).val()
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


def userform(request, formtype, id=None):
    token = gettoken()
    if token:
        user_list = getusernamelist(formtype, token)
        gradelist = getnameidlist("Grade", "title", token)
        if formtype == 'Teacher':
            form = StaffForm()
            category = "Teacher"
        elif formtype == 'Student':
            form = StudentForm()
            category = "Student"
        elif formtype == 'Parent':
            form = ParentForm()
            category = "Parent"

        if id:
            try:
                forminstance = db.child("Users").child(formtype).child(id).get(token).val()
                if formtype == "Student":
                    form = EditStudentForm(forminstance)
                elif formtype == "Parent":
                    form = EditParentForm(forminstance)
                elif formtype == "Teacher":
                    form = EditStaffForm(forminstance)

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
                    del r['password']
                    print(r)
                    user = authe.create_user_with_email_and_password(email, passw)
                    uid = user['localId']
                    db.child("Users").child(category).child(uid).set(r, token)
                    db.child("Grade").child(r["grade"]).child("Student").update({uid: "true"}, token)
                    return redirect('/mainapp/source/schooladmin/')
            except:
                message = "Unable to create account. Please try again"
                return render(request, "source/schooladmin.html", {"messg": message})

        args = {'form': form, 'items': schoolitems, 'formtype': formtype, 'grade': gradelist, 'user_list': user_list}
        return render(request, "source/form.html", args)
    else:
        return sign(request)


def getnameidlist(which, suitablename, token):
    try:
        mydata = db.child(which).get(token).val()
        idslist = list(mydata.keys())
        print(idslist)
        nameslist = []
        for i in idslist:
            nameslist.append(mydata[i][suitablename])
        print(nameslist)
        return zip(idslist, nameslist)
    except:
        pass


def getform(formtype):
    if formtype == 'Schools':
        modelform = School

    elif formtype == 'SchoolAdmin':
        modelform = SchoolAdmin

    elif formtype == 'Courses':
        modelform = Course

    return (modelform)


def allform(request, formtype, id=None):
    token = gettoken()
    if token:
        user_list = getusernamelist(formtype, token)
        all_list = getnameidlist(formtype, "title", token)
        gradelist = getnameidlist("Grade", "title", token)
        course_list = getnameidlist("Courses", "title", token)

        class AllForm(forms.ModelForm):
            class Meta:
                model = getform(formtype)
                fields = '__all__'

        if id:
            try:
                if formtype == 'SchoolAdmin':
                    forminstance = db.child("Users").child(formtype).child(id).get(token).val()
                    form = EditSchoolAdminForm(forminstance)
                else:
                    forminstance = db.child(formtype).child(id).get(token).val()
                    form = AllForm(forminstance)

            except:
                isupdate = 0
                return HttpResponse("id not valid")  # for adding new data into forms

        else:
            form = AllForm()

        if request.method == 'POST':
            form = AllForm(request.POST)
            request.POST._mutable = True
            email = request.POST.get("email")
            passw = request.POST.get("password")
            r = request.POST
            del r['csrfmiddlewaretoken']

            if form.is_valid:
                # update if request.post has id
                if id:
                    db.child(formtype).child(id).update(r, token)

                elif formtype == 'SchoolAdmin':
                    del r['password']
                    user = authe.create_user_with_email_and_password(email, passw)
                    uid = user['localId']
                    db.child("Users").child("SchoolAdmin").child(uid).set(r, token)
                else:
                    # insert if request.post doesnt have id
                    cid = db.child(formtype).push(r, token)
                    courseid = cid["name"]
                    try:  # For pushing only courseid in grade node
                        # db.child("Schools").push(r,token)
                        db.child("Grade").child(r["grade"]).child("Courses").update({courseid: "true"}, token)
                        db.child("Courses").child(courseid).update({r["grade"]}, token)
                        return redirect("/mainapp/allform/Courses/")
                    except:
                        pass

        if formtype == 'Schools':
            items = companyitems

        elif formtype == 'SchoolAdmin':
            items = companyitems

        else:
            items = schoolitems

        args = {'form': form, 'items': items, 'formtype': formtype, 'all_list': all_list, 'grade': gradelist,
                'user_list': user_list, 'course_list': course_list}
        return render(request, 'source/form.html', args)
    else:
        return sign(request)


def companyadmin(request):
    token = gettoken()
    if token:
        return render(request, 'source/companyadmin.html', {'items': companyitems})
    else:
        return sign(request)


def schooladmin(request):
    token = gettoken()
    if token:

        return render(request, 'source/schooladmin.html', {'items': schoolitems})
    else:
        return sign(request)


def studentview(request, uid):
    token = gettoken()
    if token:
        x = authe.current_user
        uid = (x['localId'])
        # courselist=student_course(x['localId'])
        return render(request, 'source/student.html', {'uid': uid})
    else:
        return sign(request)


def parent(request):
    token = gettoken()
    if token:
        x = authe.current_user
        # print(x['localId'])
        return render(request, 'source/parent.html')
    else:
        return sign(request)

def editprofile(request):
    token = gettoken()
    if token:
        user = authe.current_user
        uid = user['localId']

        forminstance = db.child("Users").child("SchoolAdmin").child(uid).get(token).val()
        if forminstance:
            form = EditSchoolAdminForm(forminstance)
            myhtml = 'adminbase.html'
            if request.method == 'POST':
                request.POST._mutable = True
                r = request.POST
                print(r)
                db.child("Users").child("SchoolAdmin").child(uid).update(r, token)
                messages.success(request, _("Profile Updated"))
            return render(request, "source/edit.html", {'form': form, 'myhtml': myhtml, 'uid':uid})

        else:
            forminstance = db.child("Users").child("Teacher").child(uid).get(token).val()
            if forminstance:
                form = EditStaffForm(forminstance)
                myhtml = 'teacherbase.html'
                if request.method == 'POST':
                    request.POST._mutable = True
                    r = request.POST
                    print(r)
                    db.child("Users").child("Teacher").child(uid).update(r, token)
                    messages.success(request, _("Profile Updated"))
                return render(request, "source/edit.html", {'form': form, 'myhtml': myhtml, 'uid':uid})
            else:
                forminstance = db.child("Users").child("Student").child(uid).get(token).val()
                if forminstance:
                    form = EditStudentForm(forminstance)
                    myhtml = 'sidebarbase.html'
                    if request.method == 'POST':
                        request.POST._mutable = True
                        r = request.POST
                        print(r)
                        db.child("Users").child("Student").child(uid).update(r, token)
                        messages.success(request, _("Profile Updated"))
                    return render(request, "source/edit.html", {'form': form, 'myhtml': myhtml, 'uid':uid})
                else:
                    forminstance = db.child("Users").child("Parent").child(uid).get(token).val()
                    if forminstance:
                        form = EditStudentForm(forminstance)
                        myhtml = 'sidebarbase.html'
                        if request.method == 'POST':
                            request.POST._mutable = True
                            r = request.POST
                            print(r)
                            db.child("Users").child("parent").child(uid).update(r, token)
                            messages.success(request, _("Profile Updated"))
                        return render(request, "source/edit.html", {'form': form, 'myhtml': myhtml, 'uid':uid})
    else:
        return sign(request)


# Tab Quiz

def tabquiz(request, uid):
    token = gettoken()
    if token:
        courselist = student_course(uid, token)
        print(quizlist)
        if uid:
            return render(request, "source/tabquiz.html", {'courselist': courselist, 'uid': uid})
        else:
            return render(request, "source/tabquiz.html", {'courselist': courselist})
    else:
        return sign(request)


def takequiz(request, uid, quizid):
    token = gettoken()
    if token:
        question_list = getrelation("Quiz", quizid, "Questions", "question", token)
        return render(request, "source/takequiz.html", {'uid': uid, 'question_list': question_list})
    else:
        return sign(request)


def quizlist(request):
    return render(request, "source/quizlist.html")


def coursequiz(request, uid, cid):
    token = gettoken()
    if token:
        quizlist = getrelation("Courses", cid, 'Quiz', 'name', token)
        return render(request, "source/coursequiz.html", {'uid': uid, 'quizlist': quizlist})
    else:
        return sign(request)


# for grade
def grade(request):
    token = gettoken()
    if token:
        gradelist = getnameidlist("Grade", "title", token)
        print(gradelist)
        if request.method == 'POST':
            request.POST._mutable = True
            r = request.POST
            del r['csrfmiddlewaretoken']
            db.child("Grade").push(r, token)
            return redirect("/mainapp/grade/")
        args = {'items': schoolitems, 'grade': gradelist}
        return render(request, "source/grade.html", args)
    else:
        return sign(request)


# For Assigning teacher to courses

def assign(request):
    token = gettoken()
    if token:
        teacher_list = getusernamelist("Teacher", token)
        course_list = getnameidlist("Courses", "title", token)
        args = {'course_list': course_list, 'teacher_list': teacher_list, 'items': schoolitems}
        if request.method == 'POST':
            request.POST._mutable = True
            r = request.POST
            del r['csrfmiddlewaretoken']
            db.child("Users").child("Teacher").child(r["teacher"]).child("Courses").update({r["course"]: "true"}, token)
            print(r["teacher"])
            db.child("Courses").child(r["course"]).child("Teacher").update({r["teacher"]: "true"}, token)
            return redirect("schooladmin")

        return render(request, "source/assigncourse.html", args)
    else:
        return sign(request)


def getrelation(which, whichid, node, suitablename, token):
    try:
        data = db.child(which).child(whichid).child(node).get(token).val()
        idlist = list(data)
        print(idlist)
        namelist = []
        for i in idlist:
            namelist.append(db.child(node).child(i).child(suitablename).get(token).val())
        print(namelist)
        return (zip(idlist, namelist))
    except:
        pass


def student_course(uid, token):
    try:
        x = db.child('Users').child('Student').child(uid).child('grade').get(token).val()
        print(x)
        stdcourse = getrelation("Grade", x, 'Courses', 'title', token)
        return stdcourse
    except:
        pass


# for teacher-course
def teacher_course(uid, token):
    try:
        data = db.child('Users').child('Teacher').child(uid).child('Courses').get(token).val()
        idlist = list(data)
        namelist = []
        for i in idlist:
            namelist.append(db.child('Courses').child(i).child('title').get(token).val())
        return (zip(idlist, namelist))
    except:
        pass


def viewcourse(request, id=None):
    token = gettoken()
    if token:
        getcid_items = getrelation("Grade", id, "Courses", "title", token)
        return render(request, "source/viewcourse.html", {'getcid_items': getcid_items, 'items': schoolitems})
    else:
        return sign(request)


# views for teacher
def teacherview(request):
    user = authe.current_user
    token = gettoken()
    if token:
        uid = user['localId']
        return render(request, 'teacher/teacherhome.html', {'uid': uid})
    else:
        return sign(request)


def courses(request,courseid=None):
    user = authe.current_user
    token = gettoken()
    if token:
        uid = user['localId']
        coursedetail = teacher_course(uid, token)

        if request.method == 'POST':
            request.POST._mutable = True
            r = request.POST
            del r['csrfmiddlewaretoken']
            cid = r['course']
            topicid = db.child("Topics").push(r, token)
            tid = topicid['name']
            # db.child('Topics').child(tid).child('Courses').update({cid: 'true'}, token)
            db.child("Courses").child(cid).child('Topics').update({tid: 'true'}, token)
            template='/mainapp/teacher/courses/'+str(cid)+'/'

            return redirect(template, uid=uid)
        if courseid:
            topicdetail = getrelation("Courses", courseid, "Topics", "title", token)
            return render(request, 'teacher/courses.html', {'courses': list(coursedetail),'topics':(topicdetail),'uid': uid})
        return render(request, 'teacher/courses.html', {'courses': list(coursedetail), 'uid': uid})
    else:
        return sign(request)


def quizcreate(request):
    token = gettoken()
    if token:
        coursedetail = getnameidlist("Courses", "title", token)
        topicdetail = getnameidlist("Topics", "title", token)
        if request.method == 'POST':
            request.POST._mutable = True
            r = request.POST
            del r['csrfmiddlewaretoken']
            x = db.child('Quiz').push(r, token)
            print(x)
            quizid = x['name']
            db.child("Courses").child(r['course']).child('Quiz').update({quizid: 'true'}, token)
            # db.child("Courses").child(r['topic']).child('quiz').update({quizid:'true'})
            db.child("Topics").child(r['topic']).child('Quiz').update({quizid: 'true'}, token)
            return redirect('quizquestion', quizid=quizid)
        return render(request, 'teacher/quizcreate.html', {'courses': coursedetail, 'topics': topicdetail})
    else:
        return sign(request)


def quizquestion(request, quizid):
    token = gettoken()
    if token:
        quizquestionlist = getrelation('Quiz', quizid, 'Questions', 'question', token)
        quizcourse=db.child("Quiz").child(quizid).child("course").get(token).val()
        quiztopic=db.child("Quiz").child(quizid).child("topic").get(token).val()
        print(quizcourse)
        allquestionlist=getrelation("Courses",quizcourse,"Questions","question",token)
        print(allquestionlist)
        if request.method == "POST":
            print(request.POST)
            request.POST._mutable = True
            r = request.POST
            del r['csrfmiddlewaretoken']
            r['course']=quizcourse
            r['topic']=quiztopic
            # if questionid then update
            try:
                qid = r['questionid']
                if r['type'] == 'mcq':
                    print(r)
                    ca = r['correctanswer']
                    r['correctanswer'] = r[ca]
                else:
                    del r['option1']
                del r['questionid']
                db.child('Questions').child(qid).update(r, token)
                data = {'question': r['question'], 'qid': qid}
                messages.success(request, _("Question Updated Succesfully"))
                return redirect('question')
            except:  # creating new question#qid=questionid
                if r['type'] == 'mcq':
                    print(r)
                    ca = r['correctanswer']
                    r['correctanswer'] = r[ca]
                else:
                    del r['option1']
                z = db.child('Questions').push(r, token)
                qid = z['name']
                # reverse relation for quiz and question
                db.child('Quiz').child(quizid).child('Questions').update({qid: 'true'}, token)
                db.child('Courses').child(quizcourse).child('Questions').update({qid: 'true'}, token)
                db.child('Topics').child(quiztopic).child('Questions').update({qid: 'true'}, token)
                data = {'question': r['question'], 'qid': qid}
            return redirect('quizquestion',quizid)
        args={'quizid': quizid, 'questionlist': quizquestionlist,'allquestionlist':allquestionlist}
        return render(request, 'teacher/question.html',args)
    else:
        return sign(request)


def question(request):
    user = authe.current_user
    token = gettoken()
    if token:
        teacher_list = db.child('Users').child('Teacher').shallow().get(token).val()
        schooladmin_list = db.child('Users').child('Admin').shallow().get(token).val()
        print(schooladmin_list)
        uid = user['localId']
        questionlist = getnameidlist("Questions", "question", token)
        if request.method == "POST":
            print(request.POST)
            request.POST._mutable = True
            r = request.POST
            del r['csrfmiddlewaretoken']
            # if questionid then update
            try:
                qid = r['questionid']
                if r['type'] == 'mcq':
                    print(r)
                    ca = r['correctanswer']
                    r['correctanswer'] = r[ca]
                else:
                    del r['option1']
                del r['questionid']
                db.child('Questions').child(qid).update(r, token)
                data = {'question': r['question'], 'qid': qid}
                messages.success(request, _("Question Updated Succesfully"))
                return redirect('question')
            except:  # creating new question#qid=questionid
                if r['type'] == 'mcq':
                    print(r)
                    ca = r['correctanswer']
                    r['correctanswer'] = r[ca]
                else:
                    del r['option1']
                z = db.child('Questions').push(r, token)
                qid = z['name']
                db.child("Courses").child(r['course']).child("Questions").update({qid:'true'},token)
                db.child("Topics").child(r['topic']).child("Questions").update({qid:'true'},token)
                data = {'question': r['question'], 'qid': qid}
                messages.success(request, _("Question Added Succesfully"))
            return redirect('question')
        if uid in list(schooladmin_list):
            coursedetail=list(getnameidlist("Courses",'title',token))
            topicdetail=list(getnameidlist("Topics",'title',token))
            print(topicdetail)
            args={'questionlist': questionlist ,'courses':coursedetail,'items': companyitems,'topics':topicdetail}
            return render(request, 'teacher/companyquestion.html')
        else:
            uid = user['localId']
            coursedetail = list(teacher_course(uid, token))
            topicdetail = list(getnameidlist("Topics", 'title', token))
            args={'questionlist': questionlist ,'courses':coursedetail,'topics':topicdetail}
            return render(request, 'teacher/rawquestion.html',args)

        # return render(request, 'teacher/question.html', {'questionlist': questionlist, 'myhtml': myhtml})
    else:
        return sign(request)


def delete(request, deleteid):
    token = gettoken()
    if token:
        if request.method == "GET" and request.is_ajax():
            print('DEleteded');
            qcourse=db.child('Questions').child(deleteid).child('course').get(token).val()
            qtopic=db.child('Questions').child(deleteid).child('topic').get(token).val()
            db.child('Questions').child(deleteid).remove(token)
            db.child('Courses').child(qcourse).child("Questions").child(deleteid).remove(token)
            db.child('Topics').child(qtopic).child("Questions").child(deleteid).remove(token)
            db.child('Questions').child(deleteid).remove(token)
            return HttpResponse("Question deleted succesfully")
    else:
        return sign(request)

def remove_from_quiz(request,quizid,qid):
    token = gettoken()
    if token:
        if request.method == "GET" and request.is_ajax():
            db.child('Quiz').child(quizid).child('Questions').child(qid).remove(token)
            return HttpResponse("Question deleted succesfully")
    else:
        return sign(request)

def questiondetail(request, questionid):
    token = gettoken()
    if token:
        if request.method == "GET" and request.is_ajax():
            detail = db.child('Questions').child(questionid).get(token).val()
            print(detail)
            return JsonResponse(detail)
    else:
        return sign(request)

def coursetopic(request,courseid):
    token = gettoken()
    if token:
        if request.method == "GET" and request.is_ajax():
            topicdetail = db.child('Courses').child(courseid).child('Topics').get(token).val()
            print(topicdetail)
            return JsonResponse(topicdetail)
    else:
        return sign(request)

def classes(request):
    return render(request, 'teacher/classes.html')


def students(request):
    return HttpResponse("HELLO")
def add_to_quiz(request,quizid,qid):
    token=gettoken()
    if token:
        db.child("Quiz").child(quizid).child('Questions').update({qid:'true'},token)
        return HttpResponse('Question added to quiz')

    else:
        return sign(request)

def getuserid(which, suitablename, token):
    try:
        data = db.child("Users").get(token).val()
        # print(data)
        idlist = list(data[which].keys())
        print(idlist)
        for i in idlist:
            student_gradeid = (data[which][i][suitablename])
        # print(student_gradeid)
        return student_gradeid
    except:
        pass
