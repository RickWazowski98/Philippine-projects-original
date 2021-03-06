#!/bin/sh
. "venv/bin/activate"
python args_get_urls_by_tab.py -tn "Malaysia condominiums"
python args_dt_dotproperty-1.py -tn "Malaysia condominiums"
python args_dt_load_to_sheet.py -tn "Malaysia condominiums"
python args_dt_dotproperty-2.py -tn "Malaysia condominiums"
python args_dt_dotproperty-mix.py -tn "Malaysia condominiums"

python args_get_urls_by_tab.py -tn "Malaysia houses"
python args_dt_dotproperty-1.py -tn "Malaysia houses"
python args_dt_load_to_sheet.py -tn "Malaysia houses"
python args_dt_dotproperty-2.py -tn "Malaysia houses"
python args_dt_dotproperty-mix.py -tn "Malaysia houses"

python args_get_urls_by_tab.py -tn "Malaysia townhouses"
python args_dt_dotproperty-1.py -tn "Malaysia townhouses"
python args_dt_load_to_sheet.py -tn "Malaysia townhouses"
python args_dt_dotproperty-2.py -tn "Malaysia townhouses"
python args_dt_dotproperty-mix.py -tn "Malaysia townhouses"