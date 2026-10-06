from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from orders.models import Order
from io import BytesIO

class OrderReceiptView(View):
    def get(self, request, ref, *args, **kwargs):
        try:
            order = Order.objects.get(ref=ref)
        except Order.DoesNotExist:
            raise Http404("Commande non trouvée")

        template = get_template('receipt.html')
        context = {'order': order}
        html = template.render(context)

        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="recu_{order.ref}.pdf"'
            return response
        return HttpResponse('Erreur lors de la génération du reçu PDF', status=400)
