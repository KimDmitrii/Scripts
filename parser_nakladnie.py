from bs4 import BeautifulSoup
import os
import pandas as pd
import zipfile

directory = r'D:\AM\tenderplan\UPD\04'
files = os.listdir(directory)




product_code = []
product_name = []
unit_code = []
unit_name = []
quantity = []
price = []
total_price = []
tax = []
tax_rate = []
tax_sum = []
total_price_tax = []
status =[]
invoice_number = []
invoice_date = []
cus_name = []
cus_addr = []
cus_inn = []
to_the_payment_document = []
shipping_document = []
sup_name = []
sup_addr = []
sup_inn = []
auction_code = []
contract = []
check_status = 0
correction_number = []
correction_date = []

# HTML-код, содержащий таблицу
#file_path = r"D:/AM/UPD/UPD_20221201_26C23337-FBB1-4810-AB19-D6661BE41F0D_20221208_F1AE7BBF-1C8B-4524-BA48-6A7AF3FD7813.html"
#file_path = f'D:/AM/UPD/Adygeja_Resp'


for f in files:
    if f.startswith("UPD") and f.endswith(".zip"):
            zip_file_path = os.path.join(directory, f)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                #print(zip_ref)
                # Assuming the HTML file inside the ZIP archive has a name starting with "UPD"
                html_files = [file for file in zip_ref.namelist() if file.startswith("UPD") and file.endswith(".html")]

                for html_file in html_files:
                    
                    with zip_ref.open(html_file) as file:
                        html_content = file.read().decode('utf-8')    
                        # Создание объекта BeautifulSoup
                        soup = BeautifulSoup(html_content, 'html.parser')
                        #print(file)
                        table_rows = soup.find_all('tr', class_='main-table')
                        data_rows = soup.find_all('tr')
                        #last_row = soup.find('td', text = 'Всего к оплате(9)')
                        last_index = None
                        for index, tr in enumerate(table_rows):
                            td_elements = tr.find_all('td')
                            if len(td_elements) > 1 and td_elements[2].get_text(strip=True) == 'Всего к оплате (9)':
                                last_index = index

                        if last_index is not None:
                            # Ограничение до последнего 'tr', содержащего 'Всего к оплате'
                            relevant_ = table_rows[3:last_index]
                            
                        try:
                            chek_status = soup.find_all('tr')[1].find('span', class_ = 'status-value').get_text(strip=True)
                        except AttributeError:
                            chek_status = 'empty'
                        if len(chek_status) == 1:
                            skipped_rows = 0  
                            for tr in relevant_:
                                
                                try:
                                    if len(tr.find_all('td')) > 1:  # Modify this condition as needed
                                        product_code.append(tr.find_all('td')[1].get_text(strip=True) if tr.find_all('td')[1] else ' ')
                                        code = tr.find_all('td')[1].get_text(strip=True)
                                        if not code.strip():  # Проверка на пустое значение
                                            print("Empty product code found!")
                                            
                                        product_name.append(tr.find_all('td')[3].get_text(strip=True) if tr.find_all('td')[3] else ' ')
                                        unit_code.append(tr.find_all('td')[5].get_text(strip=True) if tr.find_all('td')[5] else ' ')
                                        unit_name.append(tr.find_all('td')[6].get_text(strip=True) if tr.find_all('td')[6] else ' ')
                                        quantity.append(tr.find_all('td')[7].get_text(strip=True) if tr.find_all('td')[7] else ' ')
                                        price.append(tr.find_all('td')[8].get_text(strip=True) if tr.find_all('td')[8] else ' ')
                                        total_price.append(tr.find_all('td')[9].get_text(strip=True) if tr.find_all('td')[9] else ' ')
                                        tax.append(tr.find_all('td')[10].get_text(strip=True) if tr.find_all('td')[10] else ' ')
                                        tax_rate.append(tr.find_all('td')[11].get_text(strip=True) if tr.find_all('td')[11] else ' ')
                                        tax_sum.append(tr.find_all('td')[12].get_text(strip=True) if tr.find_all('td')[12] else ' ')
                                        total_price_tax.append(tr.find_all('td')[13].get_text(strip=True) if tr.find_all('td')[13] else ' ')
                                    else:
                                        # Log or print a message to track these rows that are being skipped
                                        print("Skipping row:", tr)
                                        skipped_rows += 1
                                except IndexError:
                                    # Log or print a message to track these rows causing the error
                                    print("Row skipped due to IndexError:", tr)
                                    continue  # Move to the next row after encountering the error
                                  
                            if skipped_rows > 0:
                                relevant_ = relevant_[:-skipped_rows]        
                            if chek_status == '1':
                                    #print(len(chek_status))
                                    to_the_payment_document.extend([soup.find_all('tr')[6].find('div').get_text(strip=True)] * len(relevant_))
                                    shipping_document.extend([soup.find_all('tr')[7].find('div').get_text(strip=True)] * len(relevant_))
                                    sup_name.extend([soup.find_all('tr')[8].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                    sup_addr.extend([soup.find_all('tr')[9].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                    sup_inn .extend([soup.find_all('tr')[10].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                    auction_code.extend([soup.find_all('tr')[12].find('span', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                    contract.extend([soup.find_all('div', class_= 'data-with-hint')[5].get_text(strip=True)] * len(relevant_))
                                    #contract.extend([soup.find_all('tr')[21].find('div', class_= 'data-with-hint').get_text(strip=True)] * len(table_rows[3:-1]))
                                    status.extend([soup.find_all('tr')[1].find('span', class_ = 'status-value').get_text(strip=True)] * len(relevant_))
                                    invoice_number.extend([soup.find_all('div', class_ = "data font-10")[0].get_text(strip=True)] * len(relevant_))
                                    invoice_date.extend([soup.find_all('div', class_ = "data font-10")[1].get_text(strip=True)] * len(relevant_))
                                    cus_name.extend([soup.find_all('tr')[1].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                    cus_addr.extend([soup.find_all('tr')[2].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                    cus_inn.extend([soup.find_all('tr')[3].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                    correction_number.extend([soup.find_all('div', class_ = "data font-10")[2].get_text(strip=True)] * len(relevant_))
                                    correction_date.extend([soup.find_all('div', class_ = "data font-10")[3].get_text(strip=True)] * len(relevant_))
    
                             
                            elif chek_status == '2':
                                #print(len(chek_status))
                                to_the_payment_document.extend([soup.find_all('tr')[6].find('div').get_text(strip=True)] * len(relevant_))
                                shipping_document.extend([" "] * len(relevant_))
                                sup_name.extend([soup.find_all('tr')[7].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                sup_addr.extend([soup.find_all('tr')[8].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                sup_inn.extend([soup.find_all('tr')[9].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                auction_code.extend([soup.find_all('tr')[11].find('span', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                contract.extend([soup.find_all('div', class_= 'data-with-hint')[5].get_text(strip=True)] * len(relevant_))
                                #contract.extend([soup.find_all('tr')[20].find('div', class_= 'data-with-hint').get_text(strip=True)] * len(table_rows[3:-1]))
                                cus_name.extend([soup.find_all('tr')[1].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                cus_addr.extend([soup.find_all('tr')[2].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                cus_inn.extend([soup.find_all('tr')[3].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                                status.extend([soup.find_all('tr')[1].find('span', class_ = 'status-value').get_text(strip=True)] * len(relevant_))
                                invoice_number.extend([soup.find_all('div', class_ = "data font-10")[0].get_text(strip=True)] * len(relevant_))
                                invoice_date.extend([soup.find_all('div', class_ = "data font-10")[1].get_text(strip=True)] * len(relevant_))
                                correction_number.extend([soup.find_all('div', class_ = "data font-10")[2].get_text(strip=True)] * len(relevant_))
                                correction_date.extend([soup.find_all('div', class_ = "data font-10")[3].get_text(strip=True)] * len(relevant_))

                                                        # Итерируемся по тегам tr с 4го до предпоследнего


                        else:
                            skipped_rows = 0
                            for tr in relevant_:
                                
                            #for index, tr in enumerate(table_rows[3:-1]):   
                                try:
                                    if len(tr.find_all('td')) > 1:  # Modify this condition as needed
                                        product_code.append(tr.find_all('td')[2].get_text(strip=True) if tr.find_all('td')[1] else ' ')
                                        code = tr.find_all('td')[1].get_text(strip=True)
                                        if not code.strip():  # Проверка на пустое значение
                                            print("Empty product code found!")
                                        product_name.append(tr.find_all('td')[1].get_text(strip=True) if tr.find_all('td')[3] else ' ')
                                        unit_code.append(tr.find_all('td')[3].get_text(strip=True) if tr.find_all('td')[5] else ' ')
                                        unit_name.append(tr.find_all('td')[4].get_text(strip=True) if tr.find_all('td')[6] else ' ')
                                        quantity.append(tr.find_all('td')[5].get_text(strip=True) if tr.find_all('td')[7] else ' ')
                                        price.append(tr.find_all('td')[6].get_text(strip=True) if tr.find_all('td')[8] else ' ')
                                        total_price.append(tr.find_all('td')[7].get_text(strip=True) if tr.find_all('td')[9] else ' ')
                                        tax.append(tr.find_all('td')[8].get_text(strip=True) if tr.find_all('td')[10] else ' ')
                                        tax_rate.append(tr.find_all('td')[9].get_text(strip=True) if tr.find_all('td')[11] else ' ')
                                        tax_sum.append(tr.find_all('td')[10].get_text(strip=True) if tr.find_all('td')[12] else ' ')
                                        total_price_tax.append(tr.find_all('td')[11].get_text(strip=True) if tr.find_all('td')[13] else ' ')
                                    else:
                                        # Log or print a message to track these rows that are being skipped
                                        print("Skipping row:", tr)
                                        skipped_rows += 1
                                except IndexError:
                                    # Log or print a message to track these rows causing the error
                                    print("Row skipped due to IndexError:", tr)
                                    continue  # Move to the next row after encountering the error
                                  
                            if skipped_rows > 0:
                                relevant_ = relevant_[:-skipped_rows]        
                            #print(len(chek_status))
                            status.extend([chek_status] * len(relevant_))
                            invoice_number.extend([soup.find_all('div', class_ = "data font-10")[0].get_text(strip=True)] * len(relevant_))
                            invoice_date.extend([soup.find_all('div', class_ = "data font-10")[1].get_text(strip=True)] * len(relevant_))
                            correction_number.extend([soup.find_all('div', class_ = "data font-10")[2].get_text(strip=True)] * len(relevant_))
                            correction_date.extend([soup.find_all('div', class_ = "data font-10")[3].get_text(strip=True)] * len(relevant_))
                            cus_name.extend([soup.find_all('tr')[2].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                            cus_addr.extend([soup.find_all('tr')[3].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                            cus_inn.extend([soup.find_all('tr')[4].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                            to_the_payment_document.extend([soup.find_all('tr')[7].find('div').get_text(strip=True)] * len(relevant_))
                            shipping_document.extend([soup.find_all('tr')[8].find('div').get_text(strip=True)] * len(relevant_))
                            sup_name.extend([soup.find_all('tr')[9].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                            sup_addr.extend([soup.find_all('tr')[10].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                            sup_inn.extend([soup.find_all('tr')[11].find('td', class_ = 'data').get_text(strip=True)] * len(relevant_))
                            auction_code.extend([soup.find_all('tr')[13].find('span', class_ = 'data').get_text(strip=True)] * len(relevant_))
                            contract.extend([soup.find_all('div', class_= 'data-with-hint')[5].get_text(strip=True)] * len(relevant_))
                                                        # Итерируемся по тегам tr с 4го до предпоследнего




dict = {'product_code': product_code,
        'product_name': product_name,
        'unit_code': unit_code,
        'unit_name': unit_name,
        'quantity': quantity,
        'price': price,
        'total_price': total_price,
        'tax': tax,
        'tax_rate': tax_rate,
        'tax_sum': tax_sum,
        'total_price_tax': total_price_tax,
        'status': status,
        'invoice_number': invoice_number,
        'invoice_date': invoice_date,
        'cus_name': cus_name,
        'cus_addr': cus_addr,
        'cus_inn': cus_inn,
        'to_the_payment_document': to_the_payment_document,
        'shipping_document': shipping_document,
        'sup_name': sup_name,
        'sup_addr': sup_addr,
        'sup_inn': sup_inn,
        'auction_code': auction_code,
        'contract': contract,
        'correction_number': correction_number,
        'correction_date': correction_date
        }
        
for key, value in dict.items():
    print(f"Length of {key}: {len(value)}")
# Проверяем длины списков
# Объединяем DataFrame о продуктах и DataFrame о компании
df = pd.DataFrame(dict)


# Сохраняем DataFrame в HTML
html_table = df.to_html(index=False)

# Записываем HTML в файл
with open(r'D:\AM\tenderplan\UPD\04\output_table.html', 'w', encoding='utf-8') as file:
    file.write(html_table)
        
# for key, value in dict.items():
    # print(f"Length of {key}: {len(value)}")
