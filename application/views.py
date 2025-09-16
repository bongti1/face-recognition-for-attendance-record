from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Data_student

import numpy as np
import cv2.data
import cv2
import os
from . import faceRecognition as fr

def Dashboard(request):
    conter = Data_student.objects.all().count()
    context={
        'total_std':conter
    }
    if request.user.is_authenticated:
        if request.path == "/":
            return render(request, 'index.html', context)
    else:
        return redirect(Login)
    

def Create_student(request):
    try:
        if request.method == 'POST':
            label = request.POST['floatingLabel']
            label_ = int(label)
            id = request.POST['floatingId']
            name = request.POST['floatingName']
            gender = request.POST['floatingGender']
            dob = request.POST['floatingDOB']
            tel = request.POST['floatingTelephone']
            batch = request.POST['floatingBatch']
            batch_ = int(batch)
            major = request.POST['floatingMajor']
            if Data_student.objects.filter(label=label_).exists():
                messages.add_message(request, messages.WARNING,"Saving fails, Label must be unique.")
            else:
                student = Data_student(label=label_, std_id=id, name=name, gender=gender, dob=dob, tel=tel, batch=batch_, major=major)
                CreateDataset(label_)
                student.save()
                messages.add_message(request, messages.SUCCESS ,"Save Successfully")
            return redirect(Create_student)
    except:
       pass
    return render(request, 'index.html')

def Retrieve_student(request):
   try:
       student = Data_student.objects.all()
       context={
           'students':student
       }
       return render(request, "index.html",context)
   except:
       pass
   return render(request, "index.html")

def Update_student(request, pk):
    try:
        findStudent = Data_student.objects.get(label = pk)
        str_label = str(pk)
        url ="/student/edit/"+str_label
        if request.method == "POST":
            findStudent.label = request.POST['floatingLabel']
            findStudent.std_id = request.POST['floatingId']
            findStudent.name = request.POST['floatingName']
            findStudent.gender = request.POST['floatingGender']
            findStudent.dob = request.POST['floatingDOB']
            findStudent.tel = request.POST['floatingTelephone']
            findStudent.batch = request.POST['floatingBatch']
            findStudent.major = request.POST['floatingMajor']
            if Data_student.objects.filter(label=pk).exists():
                messages.add_message(request, messages.WARNING,"Saving fails, Label must be unique.")
            else:
                findStudent.save()
                messages.add_message(request, messages.SUCCESS ,"Save Successfully")
            return redirect(Retrieve_student)
        context={
            'findStudent':findStudent,
            'edit_url':url
        }
        return render(request, "index.html", context)
    except:
        pass
    
def Delete_student(request, pk):
   try:
       delStudent = Data_student.objects.get(label = pk)
       delStudent.delete()
       Data_student.objects.all()
       return redirect(Retrieve_student)
   except:
       pass
   return redirect(Retrieve_student)


def Loading(request):
    Training_Model()
    messages.add_message(request, messages.INFO, "Training Model")
    return redirect(Create_student)
   
def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        if password == confirmPassword:
            if User.objects.filter(username = username).exists():
                messages.info(request, "Username {username} Already Exist.")
                return redirect(Register)
            elif User.objects.filter(email = email).exists():
                messages.info(request,"Email {email} Already Exist.")
                return redirect(Register)
            else:
                user = User.objects.create_user(username = username, email = email, password = password)
                user.save()
                messages.info(request, "Registration Successfully")
                return redirect(Login)
        else:
            messages.info(request, "Confirm password invalid...")
    else:
        return render(request,'pages-register.html')
    
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect(Dashboard)
        else:
            messages.info(request, 'Error Occurred')
            return render(request, 'pages-login.html')
    else:
        return render(request, 'pages-login.html')

def LogOut(request):
    logout(request)
    return redirect(Login)

def Profile(request):
    return render(request, 'profile.html')


# ================== ///////================

# Training Model Section

def Training_Model():
    test_img=cv2.imread(r'D:\Introduction_to_python\FRAMS\app\application\image\2\image0581.jpg')  #Give path to the image which you want to test
    faces_detected,gray_img=fr.faceDetection(test_img)
    faces,faceID=fr.labels_for_training_data(r'D:\Introduction_to_python\FRAMS\app\application\image') #Give path to the train-images folder which has both labeled folder as 0 and 1
    face_recognizer=fr.train_classifier(faces,faceID)
    face_recognizer.save(r'D:\Introduction_to_python\FRAMS\app\application\trainingData.yml')#It will save the trained model. Just give path to where you want to save
    name={0:"H",1:"C",2:"Ho",3:"So",4:"Som"} #Change names accordingly. If you want to recognize only one person then write:- name={0:"name"} thats all. Dont write for id number 1.
    for face in faces_detected:
        (x,y,w,h)=face
        roi_gray=gray_img[y:y+h,x:x+h]
        label,confidence=face_recognizer.predict(roi_gray)
        print ("Confidence :",confidence)
        print("label :",label)
        fr.draw_rect(test_img,face)
        predicted_name=name[label]
        fr.put_text(test_img,predicted_name,w,h)  
        if cv2.waitKey(10)==ord('q'):
            cv2.destroyAllWindows()
            return redirect(Create_student) 
    resized_img=cv2.resize(test_img,(1000,700))
    cv2.imshow("face detection ", resized_img)


# Face Recognition Section
def faceDetection(test_img):             
    gray_img=cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
    face_haar=cv2.CascadeClassifier(r'D:\Introduction_to_python\FRAMS\app\application\haarcascade_frontalface_alt.xml') #Give path to haar classifier as i have given
    faces=face_haar.detectMultiScale(gray_img,scaleFactor=1.2,minNeighbors=3)
    return faces,gray_img

#Labels for training data has been created

def labels_for_training_data(directory):
    faces=[]
    faceID=[]
    

    for path,subdirnames,filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith("."):
                print("skipping system file")
                continue
            id=os.path.basename(path)
            img_path=os.path.join(path,filename)
            print ("img_path",img_path)
            print("id: ",id)
            test_img=cv2.imread(img_path)
            if test_img is None:
                print ("Not Loaded Properly")
                continue

            faces_rect,gray_img=faceDetection(test_img)
            if len(faces_rect)!=1:
                continue
            (x,y,w,h)=faces_rect[0]
            roi_gray=gray_img[y:y+w,x:x+h]
            faces.append(roi_gray)
            faceID.append(int(id))
    return faces,faceID


#Here training Classifier is called
def train_classifier(faces,faceID):                              
    face_recognizer=cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces,np.array(faceID))
    return face_recognizer


#Drawing a Rectangle on the Face Function
def draw_rect(test_img,face):                                      
    (x,y,w,h)=face
    cv2.rectangle(test_img,(x,y),(x+w,y+h),(0,255,0),thickness=3)

#Putting text on images
def put_text(test_img,text,x,y):                                    
    cv2.putText(test_img,text,(x,y),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(255,0,0),2)



def FaceRecognition(request):
    face_recognizer=cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read(r'D:\Introduction_to_python\FRAMS\app\application\trainingData.yml')    #Give path of where trainingData.yml is saved

    cap=cv2.VideoCapture(0)   #If you want to recognise face from a video then replace 0 with video path

    name={0:"Hean MengFong",1:"Hean", 2:"Hot Hon",3:"Sochea Seyha",4:"Som Bondeth"}    #Change names accordingly.  If you want to recognize only one person then write:- name={0:"name"} thats all. Dont write for id number 1.
    while True:
        ret,test_img=cap.read()
        faces_detected,gray_img=fr.faceDetection(test_img)
        print("face Detected: ",faces_detected)
        for (x,y,w,h) in faces_detected:
            cv2.rectangle(test_img,(x,y),(x+w,y+h),(0,255,0),thickness=5)

        for face in faces_detected:
            (x,y,w,h)=face
            roi_gray=gray_img[y:y+h,x:x+h]
            label,confidence=face_recognizer.predict(roi_gray)
            print ("Confidence :",confidence)
            print("label :",label)
            fr.draw_rect(test_img,face)
            predicted_name=name[label]
            fr.put_text(test_img,predicted_name,x,y)

        resized_img=cv2.resize(test_img,(1000,700))
        cv2.imshow("Vedio Stream", resized_img)
        if cv2.waitKey(10)==ord('q'):
            cv2.destroyAllWindows()
            return redirect(Dashboard)
        
def mkDir(student_label):
    mydir =  os.mkdir(rf"D:\Introduction_to_python\FRAMS\app\application\image\{student_label}")
    return mydir
def CreateDataset(label_):
    student_label = label_
    mkDir(student_label)
    cpt = 0
    vidStream = cv2.VideoCapture(0)
    while True:
        ret, frame = vidStream.read() # read frame and return code.
        cv2.imshow("Greater then 300 photos,then press (q) to exit.", frame) # show image in window
        cv2.imwrite(rf"D:\Introduction_to_python\FRAMS\app\application\image\{student_label}\image%04i.jpg" %cpt, frame)    #Give path to  train-images/0/ and keep image%04i.jpg as it is in this line. Your images will be stored at train-images/0/ folder
        cpt += 1
        if cv2.waitKey(10)==ord('q'):
            cv2.destroyAllWindows()
            return redirect(Create_student)
            
        
       
