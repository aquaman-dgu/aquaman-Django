from django.shortcuts import render, redirect
from .forms import FishForm
from django.urls import reverse
# Create your views here.

def main_view(request):
    if request.method == 'POST':
        form = FishForm(request.POST, request.FILES)
        if form.is_valid():
            # 폼 데이터를 세션에 저장
            request.session['photo'] = form.cleaned_data['photo'].name
            request.session['length'] = form.cleaned_data['length']
            request.session['weight'] = form.cleaned_data['weight']
            request.session['feed_amount'] = form.cleaned_data['feed_amount']
            
            # 필요에 따라 recognition 또는 prediction 페이지로 리디렉션
            return redirect(reverse('recognition:recognition_view'))
    else:
        form = FishForm()
    return render(request, 'main/index.html', {'form': form})