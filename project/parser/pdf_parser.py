import re
import uuid
from datetime import datetime
import pdfplumber
from lxml import etree
from dateutil.relativedelta import relativedelta
from project.parser.regexes import INVOICE_NUM_REG, INVOICE_DATE_REG, \
    ORDER_NUM_REG, NUM_OF_PIECES_REG, TOTAL_PRICE_REG, RECYCLE_FEE_REG


class InvoiceClass:
    def __init__(self, file_name):
        self.file_name = file_name
        self.uuid = str(uuid.uuid4()).upper()
        self.invoice_number = ""
        self.orders = []
        self.date = None # type will by string in format '%d-%m-%Y'
        self.invoice_total_price = None
        self.success_parse_flag = True
        self.parsing_errors = []

    def update_date(self, date):
        # extracted date format: %d-%m-%y
        # this function change from extracted format to %d-%m-%Y format
        date_time_obj = datetime.strptime(date, '%d-%m-%y')

        new_date_format_string = date_time_obj.strftime('%Y-%m-%d')

        self.date = new_date_format_string

    def expiration_date(self):
        if self.date:
            date_time_obj = datetime.strptime(self.date, '%Y-%m-%d')

            expiration_date_datetime = date_time_obj + relativedelta(years=1)

            expiration_date_string = expiration_date_datetime.strftime('%Y-%m-%d')

            return expiration_date_string

    def isdoc_name(self):
        isdoc_name_split = self.file_name.split('/')
        isdoc_name = isdoc_name_split[-1]
        isdoc_name = re.sub(r'(pdf|PDF)', 'isdoc', isdoc_name)

        return isdoc_name

    def calculate_total_price(self):
        self.invoice_total_price = 0

        for order in self.orders:
            self.invoice_total_price += float(order.total_price_without_dph)

        self.invoice_total_price = str(round(self.invoice_total_price, 2))


class Order:
    def __init__(self, order_num, product_name, num_of_pieces, item_price_without_dph, total_price_without_dph):
        self.order_num = order_num
        self.product_name = product_name
        self.num_of_pieces = num_of_pieces
        self.item_price_without_dph = item_price_without_dph
        self.total_price_without_dph = total_price_without_dph

    def quantity(self):
        search_result = re.search(r'\d+', self.num_of_pieces)
        if search_result:
            return str(search_result.group())

    def data_ready(self):
        return self.order_num != '' and self.product_name != '' and self.num_of_pieces != '' \
            and self.item_price_without_dph != '' and self.total_price_without_dph != ''


def calculate_item_price_without_dph(num_of_pieces, total_price_without_dph):
    search_result = re.search(r'\d+', num_of_pieces)

    if search_result:
        number = int(search_result.group())

        total_price_num = float(total_price_without_dph.replace(',', '.'))

        item_price_without_dph = total_price_num / number

        item_price_without_dph = round(item_price_without_dph, 2)

        return item_price_without_dph


def parse_pdf(file_name: str) -> InvoiceClass:
    # first load pdf
    with pdfplumber.open(file_name) as pdf:
        invoice = InvoiceClass(file_name)

        # iterate through each page in pdf
        for page in pdf.pages:

            # extract text from current page
            text = page.extract_text()

            # split text to lines
            lines = text.split('\n')

            # iterate through each line
            for line in lines:

                # remove unnecessary white spaces
                line = line.strip()

                # try to find invoice number
                invoice_num_res = re.search(INVOICE_NUM_REG, line)

                # invoice number was found and it isn't set yet
                if invoice_num_res and invoice.invoice_number == "":
                    invoice_num = invoice_num_res.groups()[0]

                    invoice.invoice_number = invoice_num

                # try to find invoice date
                invoice_date_res = re.search(INVOICE_DATE_REG, line)

                # invoice date was found and it isn't set yet
                if invoice_date_res and invoice.date is None:
                    invoice_date = invoice_date_res.groups()[0]

                    invoice.update_date(invoice_date)

                # try to find order number by regex
                order_num_res = re.search(ORDER_NUM_REG, line)

                # make sure order number was found by regex
                if order_num_res:
                    # get value of order number
                    order_num = order_num_res.group().replace(' ', '')

                    # find number of pieces and total price by regexes
                    num_of_pieces_res = re.search(NUM_OF_PIECES_REG, line)
                    # item_price_without_dph_res = re.search(ITEM_PRICE_REG, line)
                    total_price_without_dph_res = re.search(TOTAL_PRICE_REG, line)

                    # make sure order has both number of pieces and total price
                    # if num_of_pieces_res and item_price_without_dph_res and total_price_without_dph_res:
                    if num_of_pieces_res and total_price_without_dph_res:
                        # get price value and value of number of pieces
                        num_of_pieces = num_of_pieces_res.groups()[-1]
                        # item_price_without_dph = item_price_without_dph_res.groups()[-2]
                        total_price_without_dph = total_price_without_dph_res.group().replace(',', '.')

                        item_price_without_dph = calculate_item_price_without_dph(num_of_pieces, total_price_without_dph)

                        # product name is between order number and number of pieces
                        product_name = line[order_num_res.end():num_of_pieces_res.start()].strip()

                        invoice.orders.append(Order(
                            order_num,
                            product_name,
                            num_of_pieces,
                            item_price_without_dph,
                            total_price_without_dph
                        ))

                    else:
                        recycle_fee_reg_res = re.search(RECYCLE_FEE_REG, line)

                        # if this is recycle fee, then all orders were successfully extracted
                        if recycle_fee_reg_res is None:
                            invoice.success_parse_flag = False
                            invoice.parsing_errors.append('Nepodarilo sa ziskať údaje o objednávke s číslom: ' + str(order_num) + ' v pdf ' + file_name)

    # make sure all invoice data are ready
    if invoice.invoice_number is None or len(invoice.orders) == 0 or invoice.date is None or invoice.success_parse_flag is False:
        invoice.success_parse_flag = False
        invoice.parsing_errors.append('Z dokumentu: ' + invoice.file_name + ' sa nedopodarili získať potrebné údaje.')

    invoice.calculate_total_price()

    return invoice


def create_is_doc(invoice: InvoiceClass) -> list[str]:
    # first load sample of this isdoc
    tree = etree.parse('sample.isdoc')  # type: ignore

    # create isdoc document from extracted invoice
    # make deepcopy of isdoc sample
    tree_copy = tree.__deepcopy__(tree)

    Invoice = tree_copy.getroot()

    # change invoice number
    ID = Invoice.xpath('ID')[0]
    ID.text = invoice.invoice_number

    # change invoice UUID
    UUID = Invoice.xpath('UUID')[0]
    UUID.text = invoice.uuid

    # change invoice date
    IssueDate = Invoice.xpath('IssueDate')[0]
    IssueDate.text = invoice.date

    # change tax date of invoice
    TaxPointDate = Invoice.xpath('TaxPointDate')[0]
    TaxPointDate.text = invoice.date

    InvoiceLines = Invoice.xpath('InvoiceLines')[0]

    # remove sample InvoiceLine from InvoiceLines
    InvoiceLine = InvoiceLines.xpath('InvoiceLine')[0]

    InvoiceLines.remove(InvoiceLine)

    total_invoice_orders = len(invoice.orders)

    creation_errors = [] # storing all error during isdoc file creation

    # add all orders in InvoiceLines
    for index in range(total_invoice_orders):
        curr_order = invoice.orders[index]

        # make sure all order data are ready
        if not curr_order.data_ready():
            creation_errors.append('Faktúre s číslom: ' + str(invoice.invoice_number) + ' chýbajú udaje pre objednávku: ' + str(curr_order.order_num))
            continue

        # firstly get all needed values
        curr_quantity = curr_order.quantity()
        curr_order_num = str(curr_order.order_num)
        curr_product_name = str(curr_order.product_name)
        curr_item_price_without_dph = str(curr_order.item_price_without_dph)
        curr_total_price_without_dph = str(curr_order.total_price_without_dph)

        # make deep copy of InvoiceLine
        InvoiceLine_Copy = InvoiceLine.__deepcopy__(InvoiceLine)

        # ID in InvoiceLine is increasing by each order in invoice
        InvoiceLine_Copy.xpath('ID')[0].text = str(index + 1)

        # set invoice quantity
        InvoiceLine_Copy.xpath('InvoicedQuantity')[0].text = curr_quantity

        # set total order price
        InvoiceLine_Copy.xpath('LineExtensionAmount')[0].text = curr_total_price_without_dph

        # set total price for current order
        InvoiceLine_Copy.xpath('LineExtensionAmountTaxInclusive')[0].text = curr_total_price_without_dph

        # this has to be 0 each time
        InvoiceLine_Copy.xpath('LineExtensionTaxAmount')[0].text = str(0)

        # set item price
        InvoiceLine_Copy.xpath('UnitPrice')[0].text = curr_item_price_without_dph

        # set item price
        InvoiceLine_Copy.xpath('UnitPriceTaxInclusive')[0].text = curr_item_price_without_dph

        Invoice_Item = InvoiceLine_Copy.xpath('Item')[0]

        # value of description is product name
        Invoice_Item.xpath('Description')[0].text = curr_product_name

        # set order num
        SellersItemIdentification = Invoice_Item.xpath('SellersItemIdentification')[0]
        SellersItemIdentification.xpath('ID')[0].text = curr_order_num

        # set order num
        SecondarySellersItemIdentification = Invoice_Item.xpath('SecondarySellersItemIdentification')[0]
        SecondarySellersItemIdentification.xpath('ID')[0].text = curr_order_num

        # set order num
        BuyersItemIdentification = Invoice_Item.xpath('BuyersItemIdentification')[0]
        BuyersItemIdentification.xpath('ID')[0].text = curr_order_num

        InvoiceLines.append(InvoiceLine_Copy)

    # changing other values for invoice
    TaxTotal = Invoice.xpath('TaxTotal')[0]
    TaxSubTotal = TaxTotal.xpath('TaxSubTotal')[0]

    # total invoice price
    TaxSubTotal.xpath('TaxableAmount')[0].text = invoice.invoice_total_price

    # total invoice price
    TaxSubTotal.xpath('TaxInclusiveAmount')[0].text = invoice.invoice_total_price

    # total invoice price
    TaxSubTotal.xpath('DifferenceTaxableAmount')[0].text = invoice.invoice_total_price

    # total invoice price
    TaxSubTotal.xpath('DifferenceTaxInclusiveAmount')[0].text = invoice.invoice_total_price

    LegalMonetaryTotal = Invoice.xpath('LegalMonetaryTotal')[0]

    # total invoice price
    LegalMonetaryTotal.xpath('TaxExclusiveAmount')[0].text = invoice.invoice_total_price

    # total invoice price
    LegalMonetaryTotal.xpath('TaxInclusiveAmount')[0].text = invoice.invoice_total_price

    # total invoice price
    LegalMonetaryTotal.xpath('DifferenceTaxInclusiveAmount')[0].text = invoice.invoice_total_price

    # total invoice price
    LegalMonetaryTotal.xpath('PayableAmount')[0].text = invoice.invoice_total_price

    # total invoice price
    LegalMonetaryTotal.xpath('DifferenceTaxExclusiveAmount')[0].text = invoice.invoice_total_price

    PaymentMeans = Invoice.xpath('PaymentMeans')[0]
    PaymentMeans_Payment = PaymentMeans.xpath('Payment')[0]
    PaymentMeans_Payment.xpath('PaidAmount')[0].text = str(0)
    PaymentMeans_Payment_Details = PaymentMeans_Payment.xpath('Details')[0]
    PaymentMeans_Payment_Details.xpath('IssueDate')[0].text = invoice.date

    # invoice number in variable symbol
    PaymentMeans_Payment_second = PaymentMeans.xpath('Payment')[1]
    PaymentMeans_Payment_second_Details = PaymentMeans_Payment_second.xpath('Details')[0]
    PaymentMeans_Payment_second_Details.xpath('VariableSymbol')[0].text = invoice.invoice_number

    # In the end don't forgot to add xmlns="http://isdoc.cz/namespace/2013" in Invoice tag
    Invoice.set('xmlns', 'http://isdoc.cz/namespace/2013')

    tree_copy.write(invoice.isdoc_name(), pretty_print=True, xml_declaration=True, encoding='utf-8')

    return creation_errors