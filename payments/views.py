from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment, Invoice
from .forms import PaymentForm, InvoiceForm

def payment_list(request):
  payments = Payment.objects.all()
  return render(request, 'payments/payment_list.html', {'payments': payments})

def payment_detail(request, pk):
  payment = get_object_or_404(Payment, pk=pk)
  return render(request, 'payments/payment_detail.html', {'payment': payment})

def payment_create(request, contract_id):
  if request.method == 'POST':
    form = PaymentForm(request.POST)
    if form.is_valid():
      payment = form.save(commit=False)
      payment.contract_id = contract_id
      payment.save()
      return redirect('payment_detail', pk=payment.pk)
  else:
    form = PaymentForm()
  return render(request, 'payments/payment_form.html', {'form': form})

def payment_update(request, pk):
  payment = get_object_or_404(Payment, pk=pk)
  if request.method == 'POST':
    form = PaymentForm(request.POST, instance=payment)
    if form.is_valid():
      form.save()
      return redirect('payment_detail', pk=payment.pk)
  else:
    form = PaymentForm(instance=payment)
  return render(request, 'payments/payment_form.html', {'form': form})

def payment_delete(request, pk):
  payment = get_object_or_404(Payment, pk=pk)
  if request.method == 'POST':
    payment.delete()
    return redirect('payment_list')

def generate_invoice(request, pk):
  payment = get_object_or_404(Payment, pk=pk)
  invoice = Invoice.objects.create(payment=payment)
  return redirect('download_invoice', pk=invoice.pk)

def download_invoice(request, pk):
  invoice = get_object_or_404(Invoice, pk=pk)
  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.pk}.pdf"'