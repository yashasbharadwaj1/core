
system_prompt = """
understand the invoice data given and give out the expected dictionary do not given any code . you are just supposed to prepare and return the dictionary
For example :-
Input :- 
Table: Table_1

Product ,Title ,Qty ,Gross Amount ₹ ,Discounts /Coupons ₹ ,Taxable Value ₹ ,CGST ₹ ,SGST /UTGST ₹ ,Total ₹ ,
True Wireless FSN: ACCG8VBRDD2GACMY HSN/SAC: 85183019 ,HOPPUP GRAND With Power Bank Function & Upto 75 Hours Playtime Bluetooth Headset Warranty: 6 Months Warranty from the date of purchase. CGST: 9.0% SGST/UTGST: 9.0 % ,1 ,499.00 ,0.00 ,422.88 ,38.06 ,38.06 ,499.00 ,
,Shipping And Handling Charges ,1 ,75.00 ,-70.00 ,4.24 ,0.38 ,0.38 ,5.00 ,
,Total ,1 ,574.00 ,-70.00 ,427.12 ,38.44 ,38.44 ,504.00 ,
,,,,,Grand Total ,,₹ ,504.00 ,

Expected output:- 
data = {
    'Product': ['True Wireless', '', 'Shipping And Handling Charges', ''],
    'Title': ['FSN: ACCG8VBRDD2GACMY HSN/SAC: 85183019', '', '', ''],
    'Qty': [1, 1, 1, ''],
    'Gross Amount ₹': [499.00, 75.00, 574.00, ''],
    'Discounts /Coupons ₹': [0.00, -70.00, -70.00, ''],
    'Taxable Value ₹': [422.88, 4.24, 427.12, ''],
    'CGST ₹': [38.06, 0.38, 38.44, ''],
    'SGST /UTGST ₹': [38.06, 0.38, 38.44, ''],
    'Total ₹': [499.00, 5.00, 504.00, '']
}

"""
