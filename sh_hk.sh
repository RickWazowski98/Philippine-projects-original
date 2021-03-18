#!/bin/sh
. "venv/bin/activate"
python args_get_urls_by_tab.py -tn "Hong Kong condominiums"
python args_dt_dotproperty-1.py -tn "Hong Kong condominiums"
python args_dt_load_to_sheet.py -tn "Hong Kong condominiums"
python args_dt_dotproperty-2.py -tn "Hong Kong condominiums"
python args_dt_dotproperty-mix.py -tn "Hong Kong condominiums"
python args_get_urls_by_tab.py -tn "Hong Kong houses"
python args_dt_dotproperty-1.py -tn "Hong Kong houses"
python args_dt_load_to_sheet.py -tn "Hong Kong houses"
python args_dt_dotproperty-2.py -tn "Hong Kong houses"
python args_dt_dotproperty-mix.py -tn "Hong Kong houses"
python args_get_urls_by_tab.py -tn "Hong Kong townhouses"
python args_dt_dotproperty-1.py -tn "Hong Kong townhouses"
python args_dt_load_to_sheet.py -tn "Hong Kong townhouses"
python args_dt_dotproperty-2.py -tn "Hong Kong townhouses"
python args_dt_dotproperty-mix.py -tn "Hong Kong townhouses"