from analyse.reader.read_pdf import process_pdf
from analyse.reader.read_txt import read_txt
from analyse.reader.read_classeur import read_classeur
from analyse.reader.read_docx import read_docx
import phonenumbers
import re
from datetime import datetime
from queries.document_queries import *

## Retrieve text
def find_extension(path):
    return path.split(".")[-1]

def retrieve_text(path: str):
    extension = find_extension(path)
    if extension in ["xlsx", "xls", "ods"]:
        text = read_classeur(path)
    elif extension in ["pdf"]:
        text = process_pdf(path)
    elif extension in ["txt", "rtf", "md"]:
        text = read_txt(path)
    elif extension in ["docx", "doc"]:
        text = read_docx(path)
    else:
        raise ValueError("Unsupported file format")
    text = text.lower().replace("\n", " ")
    return text


## Credit card
def luhn_check(card_number: str):
    card_number = card_number[::-1]
    total = 0
    for i in range (len(card_number)):
        n = int(card_number[i])
        if i % 2 != 0:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

def credit_card(text : str, data_type: str):
    credit_cards = {data_type: []}
    credit_card_regex = r'\b(?:\d[ -]*?){13,19}\b'
    cards = re.findall(credit_card_regex, text)
    if len(cards) == 0:
        return credit_cards
    for card in cards:
        card = card.replace(" ", "").replace("-", "")
        if luhn_check(card):
            credit_cards[data_type].append(card[:4]+" "+card[4:8]+" "+card[8:12]+" "+card[12:])
    return credit_cards


## Phone number
def find_phone_number(text: str, data_type: str):    
    phone_numbers = {data_type: []}
    for match in phonenumbers.PhoneNumberMatcher(text, "FR"):
        try:
            if phonenumbers.is_valid_number(match.number):
                phone_numbers[data_type].append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
        except phonenumbers.NumberParseException:
            continue
    return phone_numbers


## Simple word
def find_word_in_text(text: str, word: str):
    word = word.lower()
    if word in text:
        return True
    return False


## Regex
def find_regex_in_text(text : str, regex: str, type: str):
    r = {type: re.findall(regex, text)}

    return r

## Personal information
def find_personal_information(text: str, data_type: str, parameter: str):
    result = {data_type: []}
    all_data = get_all_information_employee(parameter)
    for data in all_data:
        if find_word_in_text(text, data[0].lower()):
            result[data_type].append(data[0])
    return result

def parse_dates(dates):
    formats = [
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y/%m/%d",
        "%Y-%m-%d",
        "%d-%m-%Y"
    ]
    
    normalized_dates = []
    for date_str in dates["Date"]:
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                normalized_dates.append(parsed_date.strftime("%Y-%m-%d"))
                break
            except ValueError:
                continue

    dates["Date"] = normalized_dates
    return dates

## Realise analyse
def realise_analyse(path: str, id: int):
    text = retrieve_text(path)
    l = []
    all_data_type = get_all_data_type()
    for data_type in all_data_type:
        if data_type[2] == "Algorithm de Luhn":
            l.append(credit_card(text, data_type[1]))
        elif data_type[2] == "Phonenumbers":
            l.append(find_phone_number(text, data_type[1]))
        elif data_type[2] == "Regex":
            if data_type[1] == "Date":
                l.append(parse_dates(find_regex_in_text(text, data_type[3], data_type[1])))
            else:
                l.append(find_regex_in_text(text, data_type[3], data_type[1]))
        elif data_type[2] == "Word":
            if find_word_in_text(text, data_type[3]):
                l.append(find_word_in_text({data_type[0] : data_type[1]}))
        elif data_type[2] == "Personal information":
            l.append(find_personal_information(text, data_type[1], data_type[3]))
    title = "Analysis for document " + str(id)
    id_analysis = insert_analysis_report(id, title=title)
    for element in l:
        for type_data in element:
            for data in element[type_data]:
                insert_sensitive_data(id_analysis, data, type_data)
    return id_analysis
        

