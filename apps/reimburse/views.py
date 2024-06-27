from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from .models import Reimburse, ReimburseLine
from .forms import ReimburseForm, LineForm

@login_required
def index(request):
    docs = Reimburse.objects.filter(user=request.user)
    return render(request, "index.html", locals())

@login_required
def waiting(request):
    docs = Reimburse.objects.filter(approver=request.user, state=Reimburse.SUBMIT)
    return render(request, "index.html", locals())

@login_required
def involved(request):
    docs = Reimburse.objects.filter(approver=request.user).exclude(
            state__in=[Reimburse.DRAFT, Reimburse.SUBMIT])
    return render(request, "index.html", locals())

@login_required
def view(request, id):
    doc = Reimburse.objects.get(id=id)
    return render(request, "view.html", locals())

@login_required
def delete(request, id):
    doc = Reimburse.objects.get(id=id)
    doc.delete()
    return redirect("reimburse-index")

@login_required
def download(request, id):
    doc = ReimburseLine.objects.get(id=id)
    cont = doc.attachment.read()
    response = HttpResponse(cont)
    response['Content-Disposition'] = 'attachment; filename=%s' % doc.attachment.name
    return response


@login_required
def submit(request, id):
    doc = Reimburse.objects.get(id=id)
    if request.user != doc.user or doc.state != Reimburse.DRAFT:
        return redirect("reimburse-index")
    doc.state = Reimburse.SUBMIT
    doc.save()
    return redirect("reimburse-view", id=id)

@login_required
def paid(request, id):
    doc = Reimburse.objects.get(id=id)
    if request.user != doc.approver or doc.state != Reimburse.SUBMIT:
        return redirect("reimburse-index")
    doc.state = Reimburse.PAID
    doc.save()
    return redirect("reimburse-view", id=id)

@login_required
def reject(request, id):
    doc = Reimburse.objects.get(id=id)
    if request.user != doc.approver or doc.state != Reimburse.SUBMIT:
        return redirect("reimburse-index")
    doc.state = Reimburse.REJECT
    doc.save()
    return redirect("reimburse-view", id=id)

@login_required
def redraft(request, id):
    doc = Reimburse.objects.get(id=id)
    if request.user != doc.user or doc.state != Reimburse.REJECT:
        return redirect("reimburse-index")
    doc.state = "RD"
    doc.save()
    return redirect("reimburse-view", id=id)

@login_required
def edit(request, id):
    instance = Reimburse.objects.get(id=id)
    form = ReimburseForm(instance=instance)
    LineFormSet = inlineformset_factory(Reimburse, ReimburseLine, extra=2, form=LineForm, fields=["item",'attachment', "quantity", "price"])
    formset = LineFormSet( instance=instance, prefix="nested")
    if request.method == "POST":
        data = request.POST.copy()
        data['user'] = request.user
        form = ReimburseForm(data,  request.FILES, instance=instance)
        if form.is_valid():
            jd = form.save()
            print(request.FILES)
            formset = LineFormSet(request.POST,  request.FILES, instance=instance, prefix="nested")
            if  formset.is_valid():
                formset.save()
                return redirect("reimburse-view", id=jd.id)
            else:
                print(formset.errors)
    return render(request, "edit.html", locals())

@login_required
def add(request):
    form = ReimburseForm()
    LineFormSet = inlineformset_factory(Reimburse, ReimburseLine, form=LineForm, fields=["item",'attachment', "quantity", "price"])
    formset = LineFormSet( prefix="nested")
    if request.method == "POST":
        data = request.POST.copy()
        data['user'] = request.user
        form = ReimburseForm(data, request.FILES)
        if form.is_valid():
            jd = form.save()
            formset = LineFormSet(data, request.FILES, instance=jd, prefix="nested")
            if  formset.is_valid():
                formset.save()
                return redirect("reimburse-view", id=jd.id)
    return render(request, "add.html", locals())
