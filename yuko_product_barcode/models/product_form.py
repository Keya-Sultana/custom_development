# -*- coding: utf-8 -*-

import math
import re
import datetime
from odoo import api, models


class ProductAutoBarcode(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        res = super(ProductAutoBarcode, self).create(vals)
        year = str(datetime.date.today().year)
        month = '{:0>2}'.format(str(datetime.date.today().month))
        ean = generate_ean(year + month + str(res.id))
        res.barcode = ean
        return res

    @api.multi
    def write(self, values):
        barcode = values.get('barcode', False)
        if barcode:
            year = str(datetime.date.today().year)
            month = '{:0>2}'.format(str(datetime.date.today().month))
            ean = generate_ean(year + month + str(self.id))
            values['barcode'] = ean

        return super(ProductAutoBarcode, self).write(values)


@api.multi
def ean_checksum(eancode):
    """returns the checksum of an ean string of length 13, returns -1 if
    the string has the wrong length"""
    if len(eancode) != 13:
        return -1
    oddsum = 0
    evensum = 0
    eanvalue = eancode
    reversevalue = eanvalue[::-1]
    finalean = reversevalue[1:]

    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total = (oddsum * 3) + evensum

    check = int(10 - math.ceil(total % 10.0)) % 10
    return check


def check_ean(eancode):
    """returns True if eancode is a valid ean13 string, or null"""
    if not eancode:
        return True
    if len(eancode) != 13:
        return False
    try:
        int(eancode)
    except:
        return False
    return ean_checksum(eancode) == int(eancode[-1])


def generate_ean(ean):
    """Creates and returns a valid ean13 from an invalid one"""
    if not ean:
        return "0000000000000"
    ean = re.sub("[A-Za-z]", "0", ean)
    ean = re.sub("[^0-9]", "", ean)
    ean = ean[:13]
    if len(ean) < 13:
        ean = ean + '0' * (13 - len(ean))
    return ean[:-1] + str(ean_checksum(ean))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


# class ProductAutoBarcodeInherit(models.Model):
#     _inherit = 'product.template'
#
#     @api.model
#     def create(self, vals):
#         res = super(ProductAutoBarcodeInherit, self).create(vals)
#         year = str(datetime.date.today().year)
#         month = '{:0>2}'.format(str(datetime.date.today().month))
#         ean = generate_ean(year + month + str(res.id))
#         res.barcode = ean
#         return res
#
#     @api.multi
#     def write(self, values):
#         barcode = values.get('barcode', False)
#         if barcode:
#             year = str(datetime.date.today().year)
#             month = '{:0>2}'.format(str(datetime.date.today().month))
#             ean = generate_ean(year + month + str(self.id))
#             values['barcode'] = ean
#         return super(ProductAutoBarcodeInherit, self).write(values)
