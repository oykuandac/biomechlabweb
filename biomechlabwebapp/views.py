from django.shortcuts import render, redirect
from biomechlabwebapp.forms import FilesForm
from biomechlabwebapp.models import Files
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from scipy import stats
import statsmodels.api as sm

import csv
import pandas as pd
import pandas
import matplotlib
import matplotlib.pyplot as plt, mpld3
import numpy as np
import numpy
import io
import urllib, base64
from peakdetect import peakdetect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



# Create your views here.
def uploadFile(request):
	if not request.user.is_authenticated:
		return HttpResponse('Bu sayfaya girmeye yetkiniz bulunmamaktadır.')
	else:
		form = FilesForm()
		if request.method == "POST":
			form = FilesForm(request.POST, request.FILES)
			if form.is_valid():
				files = form.save(commit=False)
				files.attachment =  request.FILES['attachment']
				files.save()
				return redirect('/getAllData')

		return render(request, 'index.html', {'form': form})

def retrieveData(request):
	data = Files.objects.all()
	return render(request, "fileretrieve.html", {'data': data})

def getAllData(request):
	if not request.user.is_authenticated:
		return HttpResponse('Bu sayfaya girmeye yetkiniz bulunmamaktadır.')
	else:
		data = Files.objects.all()
		return render(request, "managefiles.html", {'data': data})

def deleteData(request,id):
	if not request.user.is_authenticated:
		return HttpResponse('Bu sayfaya girmeye yetkiniz bulunmamaktadır.')
	else:
	    file = Files.objects.get(pk=id)  
	    if request.method == 'POST':         
	        file.delete()                   
	        return redirect('/getAllData')
	    return render(request, 'managefiles.html')


def retrieveDataEnglish(request):
	data = Files.objects.all()
	return render(request, "fileretrieveen.html", {'data': data})

def uploadFileEnglish(request):
	if not request.user.is_authenticated:
		return HttpResponse('Bu sayfaya girmeye yetkiniz bulunmamaktadır.')
	else:
		form = FilesForm()
		if request.method == "POST":
			form = FilesForm(request.POST, request.FILES)
			if form.is_valid():
				files = form.save(commit=False)
				files.attachment =  request.FILES['attachment']
				files.save()
				return redirect('/retrieveDataEnglish')
		return render(request, "indexen.html",{'form': form})

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "accounts/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'biomechlabwebapp',
					"uid": urlsafe_base64_encode(force_bytes(user.id)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'biomechlabreset@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="accounts/password_reset.html", context={"password_reset_form":password_reset_form})

def uploadDataset(request, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponse('Bu sayfaya girmeye yetkiniz bulunmamaktadır.')
    else:
        result = {}
        if request.method == "POST":
            """First file"""
            firstFile = request.FILES['firstFile']
            fs = FileSystemStorage(location='bland-altman media')
            firstFile.read()
            firstfilename = fs.save(firstFile.name, firstFile)
            fs.open(firstfilename)
            """Second file"""
            secondFile = request.FILES['secondFile']
            secondFile.read()
            secondfilename = fs.save(secondFile.name, secondFile)
            fs.open(secondfilename)
            """Third file"""
            thirdFile = request.FILES['thirdFile']
            thirdFile.read()
            thirdfilename = fs.save(thirdFile.name, thirdFile)
            fs.open(thirdfilename)
            """Fourth file"""
            fourthFile = request.FILES['fourthFile']
            fourthFile.read()
            fourthfilename = fs.save(fourthFile.name, fourthFile)
            fs.open(fourthfilename)
            """Fifth file"""
            fifthFile = request.FILES['fifthFile']
            fifthFile.read()
            fifthfilename = fs.save(fifthFile.name, fifthFile)
            fs.open(fifthfilename)
            """Sixth file"""
            sixthFile = request.FILES['sixthFile']
            sixthFile.read()
            sixthfilename = fs.save(sixthFile.name, sixthFile)
            fs.open(sixthfilename)
            context = {}

            """Qualysis FILES"""

            firstdf = pd.read_csv(fs.open(firstfilename),skiprows=1,sep='\t')
            seconddf = pd.read_csv(fs.open(secondfilename),skiprows=1,sep='\t')
            thirddf = pd.read_csv(fs.open(thirdfilename),skiprows=1,sep='\t')

            """SMARTSUIT FILES"""

            fourthdf = pd.read_csv(fs.open(fourthfilename))
            fifthdf = pd.read_csv(fs.open(fifthfilename))
            sixthdf = pd.read_csv(fs.open(sixthfilename))

            """QUALISYS ARRAYS"""
            firstArr, secondArr, thirdArr = qualisys_data(firstdf, seconddf, thirddf, firstfilename)

            """SMARTSUIT ARRAYS"""

            fourthArr, fifthArr, sixthArr = smartsuit_data(fourthdf, fifthdf, sixthdf, fourthfilename, firstfilename)


            if "_GAIT_" not in firstfilename:

                rom1, rom4 = findPeaks(firstArr, fourthArr)
                rom2, rom5 = findPeaks(secondArr, fifthArr)
                rom3, rom6 = findPeaks(thirdArr, sixthArr)
                result1 = numpy.concatenate((rom1, rom2, rom3), axis=0)
                result2 = numpy.concatenate((rom4, rom5, rom6), axis=0)
                graph = bland_altman_plot(result1, result2)
                context = {'output':graph}
            else:
                for i in range(0,3):
                    rom1, rom4 = findPeaks(firstArr[i], fourthArr[i])
                    rom2, rom5 = findPeaks(secondArr[i], fifthArr[i])
                    rom3, rom6 = findPeaks(thirdArr[i], sixthArr[i])
                    result1 = numpy.concatenate((rom1, rom2, rom3), axis=0)
                    result2 = numpy.concatenate((rom4, rom5, rom6), axis=0)
                    graph = bland_altman_plot(result1, result2)
                    """ 3 tane grafik çıkmalı"""
                    context = {'output':graph} 


            return render(request, 'dataset.html', context)
    return render(request, 'dataset.html')

def qualisys_data(firstdf, seconddf, thirddf, firstfilename):

    """Qualysis DLA AND GAIT"""

    if "GAIT" not in firstfilename:
        if "_HIP_" in firstfilename:
            if "_FE_" in firstfilename:
                firstdf = firstdf[['X ']]
                seconddf = seconddf[['X ']]
                thirddf = thirddf[['X ']]
            elif "_ABD_" in firstfilename:
                firstdf = firstdf[['Y ']]
                seconddf = seconddf[['Y ']]
                thirddf = thirddf[['Y ']]
            else:
                firstdf = firstdf[['Z ']]
                seconddf = seconddf[['Z ']]
                thirddf = thirddf[['Z ']]
        elif "_KNE_" in firstfilename or "_ANK_" in firstfilename:
                firstdf = firstdf[['X ']]
                seconddf = seconddf[['X ']]
                thirddf = thirddf[['X ']]
        

        firstdf = pd.DataFrame(firstdf)
        firstArr = firstdf.to_numpy().ravel()

        seconddf = pd.DataFrame(seconddf)		
        secondArr = seconddf.to_numpy().ravel()

        thirddf = pd.DataFrame(thirddf)		
        thirdArr = thirddf.to_numpy().ravel()

        
    else:
        firstdf = firstdf[['X ','Y ','Z ']]
        seconddf = seconddf[['X ','Y ','Z ']]
        thirddf = thirddf[['X ','Y ','Z ']]

        firstdf = pd.DataFrame(firstdf)
        firstArr = np.transpose(firstdf.to_numpy())

        seconddf = pd.DataFrame(seconddf)
        secondArr = np.transpose(seconddf.to_numpy())

        thirddf = pd.DataFrame(thirddf)        
        thirdArr = np.transpose(thirddf.to_numpy())

    return firstArr, secondArr, thirdArr

def smartsuit_data(fourthdf, fifthdf, sixthdf, fourthfilename, firstfilename):

    """ SMARTSUIT DLA AND GAIT"""

    left_or_right = " "
    if "_LEFT_" in fourthfilename:
        left_or_right = "Left"
    else:
        left_or_right = "Right"
            
    if "GAIT" not in fourthfilename:
        if "_HIP_" in fourthfilename:
            if "_FE_" in fourthfilename:
                fourthdf = fourthdf[[left_or_right+'Hip_flexion']]
                fifthdf = fifthdf[[left_or_right+'Hip_flexion']]
                sixthdf = sixthdf[[left_or_right+'Hip_flexion']]
            elif "_ABD_" in firstfilename:
                fourthdf = fourthdf[[left_or_right+'Hip_adduction']]
                fifthdf = fifthdf[[left_or_right+'Hip_adduction']]
                sixthdf = sixthdf[[left_or_right+'Hip_adduction']]
            else:
                fourthdf = fourthdf[[left_or_right+'Hip_external_rotation']]
                fifthdf = fifthdf[[left_or_right+'Hip_external_rotation']]
                sixthdf = sixthdf[[left_or_right+'Hip_external_rotation']]
        elif "_KNE_" in fourthfilename:
            fourthdf = fourthdf[[left_or_right+'Knee_flexion']]
            fifthdf = fifthdf[[left_or_right+'Knee_flexion']]
            sixthdf = sixthdf[[left_or_right+'Knee_flexion']]
        elif "_ANK_" in fourthfilename:
            fourthdf = fourthdf[[left_or_right+'Ankle_dorsiflexion']]
            fifthdf = fifthdf[[left_or_right+'Ankle_dorsiflexion']]
            sixthdf = sixthdf[[left_or_right+'Ankle_dorsiflexion']]
        

        fourthdf = pd.DataFrame(fourthdf)		
        fourthArr = fourthdf.to_numpy().ravel()

        fifthdf = pd.DataFrame(fifthdf)		
        fifthArr = fifthdf.to_numpy().ravel()

        sixthdf = pd.DataFrame(sixthdf)		
        sixthArr = sixthdf.to_numpy().ravel()
    else:
        
        if "_HIP_" in firstfilename:
            fourthdf = fourthdf[[left_or_right+'Hip_flexion', left_or_right+'Hip_adduction',left_or_right+'Hip_external_rotation']]
            fifthdf = fifthdf[[left_or_right+'Hip_flexion', left_or_right+'Hip_adduction',left_or_right+'Hip_external_rotation']]
            sixthdf = sixthdf[[left_or_right+'Hip_flexion', left_or_right+'Hip_adduction',left_or_right+'Hip_external_rotation']]
        elif "_KNE_" in firstfilename:
            fourthdf = fourthdf[[left_or_right+'Knee_flexion', left_or_right+'Knee_adduction',left_or_right+'Knee_external_rotation']]
            fifthdf = fifthdf[[left_or_right+'Knee_flexion', left_or_right+'Knee_adduction',left_or_right+'Knee_external_rotation']]
            sixthdf = sixthdf[[left_or_right+'Knee_flexion', left_or_right+'Knee_adduction',left_or_right+'Knee_external_rotation']]
        elif "_ANK_" in firstfilename:
            fourthdf = fourthdf[[left_or_right+'Ankle_dorsiflexion', left_or_right+'Ankle_inversion',left_or_right+'Ankle_internal_rotation']]
            fifthdf = fifthdf[[left_or_right+'Ankle_dorsiflexion', left_or_right+'Ankle_inversion',left_or_right+'Ankle_internal_rotation']]
            sixthdf = sixthdf[[left_or_right+'Ankle_dorsiflexion', left_or_right+'Ankle_inversion',left_or_right+'Ankle_internal_rotation']]
        
        fourthdf = pd.DataFrame(fourthdf)        
        fourthArr = np.transpose(fourthdf.to_numpy())
        
        fifthdf = pd.DataFrame(fifthdf)        
        fifthArr = np.transpose(fifthdf.to_numpy())
        
        sixthdf = pd.DataFrame(sixthdf)        
        sixthArr = np.transpose(sixthdf.to_numpy())
    
    return fourthArr, fifthArr, sixthArr


def findPeaks(arr1, arr2):
    peaks1 = peakdetect(arr1, lookahead=20)
    peaks2 = peakdetect(arr2, lookahead=20)
    size_max1 = len(peaks1[0])
    size_min1 = len(peaks1[1])
    size_max2 = len(peaks2[0])
    size_min2 = len(peaks2[1])

    result1_max = []
    result1_min = []
    result2_max = []
    result2_min = []

    max_difference = abs(size_max1 - size_max2)
    min_difference = abs(size_min1 - size_min2)

    for i in range(0,max_difference):
        if size_max1 > size_max2:
            del peaks1[0][-1]
        else:
            del peaks2[0][-1]

    for i in range(0,min_difference):    
        if size_min1 > size_min2:
            del peaks1[1][-1]
        else:
            del peaks2[1][-1]

    for j in range(0, len(peaks1[0])):
        result1_max.append(peaks1[0][j][1])
        result2_max.append(peaks2[0][j][1])

    for i in range(0, len(peaks1[1])):
        result1_min.append(peaks1[1][i][1])
        result2_min.append(peaks2[1][i][1])

    result1 = np.concatenate((result1_max, result1_min), axis=0)
    result2 = np.concatenate((result2_max, result2_min), axis=0)
 
    return findRom(result1, result2)

def findRom(arr1, arr2):
    index = int(len(arr1)/2)
    rom1 = []
    rom2 = []
    for i in range(0, index):
        rom1.append(arr1[i] - arr1[index+i])
        rom2.append(arr2[i] - arr2[index + i])

    return rom1, rom2

def bland_altman_plot(data1, data2, *args, **kwargs):
    data1 = np.asarray(data1)
    data2 = np.asarray(data2)
    mean = np.mean([data1, data2], axis=0)
    diff = data1 - data2
    md = np.mean(diff)
    sd = np.std(diff, axis=0)
    xmin = min(mean)
    xmax = max(mean)
    fig, ax = plt.subplots()
    plt.title("Bland - Altman Plot", fontsize=20)
    plt.scatter(mean, diff, *args, **kwargs)
    plt.hlines(y = md + 1.96*sd, xmin = xmin, xmax = xmax, color='gray', linestyle='--')
    plt.hlines(y = md, xmin = xmin, xmax = xmax, color='gray', linestyle='--')
    plt.hlines(y = md - 1.96*sd, xmin = xmin, xmax = xmax, color='gray', linestyle='--')
    graph = mpld3.fig_to_html(fig)
    return graph