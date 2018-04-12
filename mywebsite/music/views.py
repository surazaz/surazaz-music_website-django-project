#using generic views
from django.views import generic
from .models import Album
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
#even after chane password continue session
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.views.generic import View
from .forms import UserForm,EditProfileForm
class IndexView(generic.ListView):
	template_name='music/index.html'

	def get_queryset(self):
		return Album.objects.all()

class DetailView(generic.DetailView):
	model=Album
	template_name='music/detail.html'

class AlbumCreate(CreateView):
	model=Album
	fields='__all__'

class AlbumUpdate(UpdateView):
	model=Album
	fields='__all__'

class AlbumDelete(DeleteView):
	model=Album
	success_url=reverse_lazy('music:index')
# def register(request):
# 	if request.method=='POST':
# 		form=UserCreationForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('/music')
# 	else:
# 		form=UserCreationForm()

# 		args={'form':form}
# 		return render(request, 'music/registration_form.html',args)
def profile(request):
	args={'user':request.user}
	return render(request,'music/profile.html',args)

def edit_profile(request):
		if request.POST:
			form=EditProfileForm(request.POST,instance=request.user)

			if form.is_valid():
				form.save()
				return render(request,'music/profile.html')


		else:
			form=EditProfileForm(instance=request.user)
			args={'form':form}
		return render(request,'music/editprofile.html',args)


def changepassword(request):
	if request.POST:
			form=PasswordChangeForm(data=request.POST,user=request.user)

			if form.is_valid():
				form.save()
				update_session_auth_hash(request,form.user)
				return render(request,'music/profile.html')
			else:
				return render(request,'music/changepassword.html',{'form':form})


	else:
		form=PasswordChangeForm(user=request.user)
		args={'form':form}
		return render(request,'music/changepassword.html',args)





class UserFormView(View):
	form_class=UserForm
	template_name='music/registration_form.html'
	#get method to give just a blank form so,none is passed,but request.post in post method
	def get(self,request):
		form=self.form_class(None)
		return render(request,self.template_name,{'form':form})

	def post(self,request):
			form=self.form_class(request.POST)

			if form.is_valid():
				user=form.save(commit=False)
				username=form.cleaned_data['username']

				password=form.cleaned_data['password']
				user.set_password(password)
				user.save()

				user=authenticate(username=username,password=password)
				if user is not None:
					if user.is_active:
						login(request,user)
						return redirect('music:index')

			return render(request,self.template_name,{'form':form})

# from django.shortcuts import render,get_object_or_404
# from django.http import HttpResponse
# from django.http import Http404
# from .models import Album,Song
# #connecting to database
# # def index(request):
# # 	a=Album.objects.all()
# # 	context={
# # 	'a':a
# # 	}
# # 	# html=""
# # 	# for b in a:
# # 	# 	url='/music/'+str(b.id)+'/'
# # 	# 	html+='<a href="'+url+'">'+str(b.id)+b.album_title+'</a><br>'
# # 	return render(request,"music/index.html",context)
# # def detail(request,album_id):
# # 	#album_id is the variable from urls.py
# # 	# try:
# # 	# 	z=Album.objects.get(pk=album_id)
# # 	# except Album.DoesNotExist:
# # 	# 	raise Http404("Album does not exist")
# # 	#all above can be written in 1 single code below by just adding in import
# # 	album=get_object_or_404(Album,pk=album_id)
# # 	return render(request,'music/detail.html',{'album':album})

# # def favourite(request,album_id):
# # 	album=get_object_or_404(Album,pk=album_id)
# # 	try:
# # 		r=request.POST['song']
# # 		print(r)
# # 		selected_song=album.song_set.get(pk=request.POST['song'])
# # 	except (KeyError,Song.DoesNotExist):
# # 		return render(request,'music/detail.html',{'album':album,'error_message':"you did not select a valid song"})
# # 	else:

# # 		print("suraj")
# # 		selected_song.is_fav=True

# # 		selected_song.save()


# # 		return render(request,"music/detail.html",{'album':album})
