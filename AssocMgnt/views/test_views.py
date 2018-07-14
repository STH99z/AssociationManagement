from django.shortcuts import render


def test_top(request):
    return render(request, 'top.html', context={})
