#!/bin/sh
. "venv/bin/activate"
python args_get_urls_by_tab.py -tn "Myanmar condominiums"
python args_dt_dotproperty-1.py -tn "Myanmar condominiums"
python args_dt_load_to_sheet.py -tn "Myanmar condominiums"
python args_dt_dotproperty-2.py -tn "Myanmar condominiums"
python args_dt_dotproperty-mix.py -tn "Myanmar condominiums"
python args_get_urls_by_tab.py -tn "Myanmar houses"
python args_dt_dotproperty-1.py -tn "Myanmar houses"
python args_dt_load_to_sheet.py -tn "Myanmar houses"
python args_dt_dotproperty-2.py -tn "Myanmar houses"
python args_dt_dotproperty-mix.py -tn "Myanmar houses"
python args_get_urls_by_tab.py -tn "Myanmar townhouses"
python args_dt_dotproperty-1.py -tn "Myanmar townhouses"
python args_dt_load_to_sheet.py -tn "Myanmar townhouses"
python args_dt_dotproperty-2.py -tn "Myanmar townhouses"
python args_dt_dotproperty-mix.py -tn "Myanmar townhouses"