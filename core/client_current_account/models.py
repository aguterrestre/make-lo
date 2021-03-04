from django.db import models
from django.forms import model_to_dict

from core.sale.models import Ticket


class ClientCurrentAccount(models.Model):
    """ Modelo para administrar los comprobantes de ventas en cuenta corriente de cliente. """
    STATUS_TICKET_CURRENT_ACCOUNT = [
        ('paid', 'Pagado'),
        ('owed', 'Adeudado'),
    ]

    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT, verbose_name='Comprobante')
    balance = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Saldo')
    status = models.CharField(max_length=10, choices=STATUS_TICKET_CURRENT_ACCOUNT, verbose_name='Situación')

    def __str__(self):
        return ("{}-{:04d}-{:08d}".format(self.ticket.get_letter_display(), self.ticket.center.number,
                self.ticket.number))

    def toJSON(self):
        item = model_to_dict(self, exclude=['ticket'])
        item['status'] = self.get_status_display()
        return item

    class Meta:
        verbose_name = 'Cuenta Corriente de Cliente'
        verbose_name_plural = 'Cuenta Corriente de Clientes'
        ordering = ['id']


class ClientReceipt(models.Model):
    """
    Modelo para administrar los recibos de cliente.
    Aquí se podrá conocer el movimiento de fondo relacionado al recibo.
    """
    STATUS_CLIENT_RECEIPT = [
        ('earring', 'Pendiente'),
        ('compliment', 'Cumplido'),
    ]

    total = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Total')
    balance = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Saldo')
    status = models.CharField(max_length=10, choices=STATUS_CLIENT_RECEIPT, verbose_name='Situación')

    def __str__(self):
        return ("C-0031-00000001")
        # return ("{}-{:04d}-{:08d}".format(self.get_letter_display(), self.center.number, self.number))

    def toJSON(self):
        item = model_to_dict(self)
        item['status'] = self.get_status_display()
        return item

    class Meta:
        verbose_name = 'Recibo de Cliente'
        verbose_name_plural = 'Recibos de Clientes'
        ordering = ['id']


class ClientReceiptDetail(models.Model):
    """
    Modelo para administrar los renglones de recibo de cliente.
    Aquí se mantendrá la relación entre recibo y comprobante de venta.
    """
    client_receipt = models.ForeignKey(ClientReceipt, on_delete=models.PROTECT)
    ticket_receipt = models.ForeignKey(Ticket, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Importe afectación')

    def __str__(self):
        return ("C-0031-00000001")
        # return ("{}-{:04d}-{:08d}".format(self.get_letter_display(), self.center.number, self.number))

    def toJSON(self):
        item = model_to_dict(self, exclude=['client_receipt', 'ticket_receipt'])
        return item

    class Meta:
        verbose_name = 'Detalle de Recibo de Cliente'
        verbose_name_plural = 'Detalle de Recibos de Clientes'
        ordering = ['id']
