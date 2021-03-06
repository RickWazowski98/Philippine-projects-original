import logging
import json
import time
import requests
from bs4 import BeautifulSoup
from helpers import headers, headers_xml, clear_ph_peso


def get_data_condo(url):
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            print('status_code', r.status_code)
            return None
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            condo_name = soup.find('div', {'class': 'row top-navigation-bar add-padding'}).find('a').text.strip()
        except:
            return None
        try:
            developer_name = soup.find('div', {'class': 'col-sm-6 nav-top-btngroups text-right'}).find('li').find('p').text.strip()
        except:
            developer_name = ''
        """
        locations = soup.find('div', {'class': 'locations'}).find('small').text.strip()
        try:
            city, province = locations.split(', ')
        except ValueError:
            province = locations
            city = ''
        area = " ".join(soup.find('ol', {'class': 'breadcrumb'}).find_all('li')[-2].text.split())
        """
        breadcrumbs = soup.find('ol', {'class': 'breadcrumb'}).find_all('li')
        province = breadcrumbs[3].text.strip()
        if len(breadcrumbs)>5:
            city = breadcrumbs[4].text.strip()
        else:
            city = ''
        if len(breadcrumbs)>6:
            area = breadcrumbs[5].text.strip()
        else:
            area = ''

        try:
            # total_units = soup.find('div', {'class': 'col-md-12 col-lg-8 project-content'}).find('section').text.strip().split('contains ')[1].split(' total')[0]
            total_units_raw = soup.find('div', {'class': 'col-md-12 col-lg-8 project-content'}).find('section').text.strip().split(' total units')[0].split(' ')[-1]
            if any(char.isdigit() for char in total_units_raw):
                total_units = total_units_raw
            else:
                total_units = ''
        except:
            total_units = ''
        try:
            units_for_rent = soup.find('a', {'id': 'open-tab-rent'}).text.strip().split(' ')[0]
        except:
            units_for_rent = ''
        """
        try:
            start_from_block = soup.find('div', {'class': 'header-line-3'})
            if start_from_block.find('a', {'id':'open-tab-rent'}):
                start_from_str = start_from_block.find_all('span', {'class': 'txt-orange'})[-1].text.strip()
                start_from = start_from_str.split('from ')[1]
                start_from = clear_ph_peso(start_from)
            else:
                start_from = ''
        except:
            start_from = ''
        """
        number_of_studios = scrape_room_types_prices(soup)
        start_from, sqm = scrape_rent_units_listing(soup)
        lowest_ask_price, sqm_ask = scrape_rent_sale_listing(soup)
        other_projects_nearby = scrape_other_projects_nearby(soup)
        popular_condos_in_area = scrape_popular_condos_in_area(soup)
        room_types_prices = scrape_room_types_prices_ext(soup)

        s_n_of_units_for_rent, s_av_rent, s_av_ask_price, bd1_n_of_units_for_rent,bd1_av_rent,bd1_av_ask_price,bd2_n_of_units_for_rent,bd2_av_rent,bd2_av_ask_price,bd3_n_of_units_for_rent,bd3_av_rent,bd3_av_ask_price,bd4_n_of_units_for_rent,bd4_av_rent,bd4_av_ask_price = '','','','','','','','','','','','','','',''
        s_n_of_units_for_sale, bd1_n_of_units_for_sale, bd2_n_of_units_for_sale, bd3_n_of_units_for_sale, bd4_n_of_units_for_sale = '', '', '', '', ''
        s_size, bd1_size, bd2_size, bd3_size, bd4_size = '','','','',''

        for t in room_types_prices:
            if t['type'] == 'Studio':
                s_size = t['size']
                s_n_of_units_for_rent = t['number of units for rent']
                s_av_rent = t['average rent']
                s_av_ask_price = t['average ask price']
                s_n_of_units_for_sale = t['number of units for sale']
            if t['type'] == '1 Bedroom':
                bd1_size = t['size']
                bd1_n_of_units_for_rent = t['number of units for rent']
                bd1_av_rent = t['average rent']
                bd1_av_ask_price = t['average ask price']
                bd1_n_of_units_for_sale = t['number of units for sale']
            if t['type'] == '2 Bedrooms':
                bd2_size = t['size']
                bd2_n_of_units_for_rent = t['number of units for rent']
                bd2_av_rent = t['average rent']
                bd2_av_ask_price = t['average ask price']
                bd2_n_of_units_for_sale = t['number of units for sale']
            if t['type'] == '3 Bedrooms':
                bd3_size = t['size']
                bd3_n_of_units_for_rent = t['number of units for rent']
                bd3_av_rent = t['average rent']
                bd3_av_ask_price = t['average ask price']
                bd3_n_of_units_for_sale = t['number of units for sale']
            if t['type'] == '4 Bedrooms':
                bd4_size = t['size']
                bd4_n_of_units_for_rent = t['number of units for rent']
                bd4_av_rent = t['average rent']
                bd4_av_ask_price = t['average ask price']
                bd4_n_of_units_for_sale = t['number of units for sale']

        print(condo_name, developer_name, city, province, area, total_units, units_for_rent, number_of_studios, start_from, sqm)
        print(lowest_ask_price, sqm_ask)
        print(other_projects_nearby)
        print(popular_condos_in_area)

        graph_link = resolve_graph_link(url)
        print(graph_link)
        median_rent_price_sqm, median_sale_price_sqm, earliest_median_sale_price_sqm, earliest_month, earliest_median_rent_price_sqm, earliest_month_1 = get_data_graph(graph_link)
        print('DEBUG s_n_of_units_for_rent:', s_n_of_units_for_rent)
        
        try:
            gps_str = soup.find('a', {'id': 'go-to-map-mobile'}).find('img')['src'].split('map_')[1].split('.jpg')[0]
            gps_lat, gps_long = gps_str.split('_')
        except:
            gps_lat, gps_long = '', ''
        
        result_bulk_1 = {
            'url': url,
            'condo_name': condo_name,
            'developer_name': developer_name,
            'province': province,
            'city': city
        }
        result_bulk_2 = {
            'area': area,
        }
        result_bulk_3 = {
            'median_rent_price_sqm': median_rent_price_sqm, # L
            's_size': s_size, #
            'bd1_size': bd1_size,
            'bd2_size': bd2_size,
            'bd3_size': bd3_size,
            'bd4_size': bd4_size, # Q
            'median_sale_price_sqm': median_sale_price_sqm,
            's_n_of_units_for_sale': s_n_of_units_for_sale,
            'bd1_n_of_units_for_sale': bd1_n_of_units_for_sale,
            'bd2_n_of_units_for_sale': bd2_n_of_units_for_sale,
            'bd3_n_of_units_for_sale': bd3_n_of_units_for_sale,
            'bd4_n_of_units_for_sale': bd4_n_of_units_for_sale, # W
            'earliest_median_rent_price_sqm': earliest_median_rent_price_sqm, # X
            'earliest_month_1': earliest_month_1,
            'earliest_median_sale_price_sqm': earliest_median_sale_price_sqm, # Z
            'earliest_month': earliest_month,
            'total_units': total_units, # AB col
            'part2_28_09-1': s_n_of_units_for_rent,
            'part2_28_09-2': check_outlier(s_av_rent,0),
            'part2_28_09-3': check_outlier(s_av_ask_price,0),
            'part2_28_09-4': bd1_n_of_units_for_rent,
            'part2_28_09-5': check_outlier(bd1_av_rent,0),
            'part2_28_09-6': check_outlier(bd1_av_ask_price,0),
            'part2_28_09-7': bd2_n_of_units_for_rent,
            'part2_28_09-8': check_outlier(bd2_av_rent,0),
            'part2_28_09-9': check_outlier(bd2_av_ask_price,0),
            'part2_28_09-10': bd3_n_of_units_for_rent,
            'part2_28_09-11': check_outlier(bd3_av_rent,0),
            'part2_28_09-12': check_outlier(bd3_av_ask_price,0),
            'part2_28_09-13': bd4_n_of_units_for_rent,
            'part2_28_09-14': check_outlier(bd4_av_rent,0),
            'part2_28_09-15': check_outlier(bd4_av_ask_price,0),
            'start_from': start_from, # Lowest rent # AR col
            'sqm': sqm,
            'lowest_ask_price': lowest_ask_price, # AT col
            'sqm_ask': sqm_ask,
            'number_of_studios': number_of_studios,
            'lat': gps_lat,
            'long': gps_long,
            'other_projects_nearby': other_projects_nearby,
        }

        """
        NOT IN USE FOR NOW:    
            'units_for_rent': units_for_rent,
            
            
            
            
            
            
            
            
            'popular_condos_in_area': popular_condos_in_area,
            'spare_1': '',
            'spare_2': '',
            
            
            
            
        }
        """
        """
        result_gps_and_others_13_02_20 = {
            
            
            'spare_1': '',
            
            
            
            
        }
        print('result_gps_and_others_13_02_20', result_gps)
        """

        return result_bulk_1, result_bulk_2, result_bulk_3
    except requests.exceptions.RequestException as e:
        print(e)
        return None, None, None

def scrape_room_types_prices(soup):
    # 23 Oct: Can you do this one too? Please return "Studio" if there is a studio unit for sale. If not, please return "1BR" if there is a 1BR unit for sale. If also not, please return nothing.
    """
    try:
        table = soup.find('div', {'class': 'container-table'}).find_all('div', {'class': 'column text-center'})
        for row in table:
            type_name = row.find('div', {'class': 'cell'}).text.strip()
            if type_name == 'Studio' or '1 Bedroom':
                return row.find_all('div', {'class': 'cell'})[-1].text.strip().split('For rent:')[1].split('(')[1].split('unit')[0].strip()

        return 0
    
    except:
        return ''
    """
    try:
        table = soup.find('div', {'class': 'container-table'}).find_all('div', {'class': 'column text-center'})
        for row in table:
            type_name = row.find('div', {'class': 'cell'}).text.strip()
            if type_name == 'Studio':
                return 'Studio'
            if type_name == '1 Bedroom':
                return '1BR'

        return ''
    
    except:
        return ''

def scrape_rent_units_listing(soup):
    try:
        table = soup.find_all('tr', {'data-tenure': 'rent'})
        # temporarily turn off this filter 
        min_price = 10000000000
        num_check_for_outlier = 9999

        for row in table:
            price_row_text = row.find('span', {'class': 'price'}).text
            price_str = price_row_text.split()[1]
            # if ',000' not in price_str:
            #     price_str = '{},000'.format(price_str)
            if any(char.isdigit() for char in price_str):# and '.' not in price_str:
                if ' - ' in price_row_text:
                    price_str_multiplied = '{}000'.format(price_str)
                    price_int = int(price_str_multiplied.replace('.' , ''))
                    print('MULTIPLIED', price_int)
                else:
                    print('YES', price_str)
                    price_int = int(price_str.replace(',' , ''))
                    print(price_int)

                if price_int < min_price: # and price_int >= 7000: # 26.10 filter >=7000
                # if price_int < min_price and price_int > num_check_for_outlier: -- # temporarily turn off this filter 
                    sqm = row.find_all('td')[1].text.split()[0].strip()
                    min_price = price_int
        print(min_price, sqm)
        return min_price, sqm
    
    except:
        return '',''

def scrape_rent_sale_listing(soup):
    try:
        table = soup.find_all('tr', {'data-tenure': 'sale'})
        # temporarily turn off this filter 
        min_price = 10000000000
        num_check_for_outlier = 999999

        for row in table:
            price_str = row.find('span', {'class': 'price'}).text.split()[1]
            if ',' in price_str:
                price_int = int(price_str.replace(',' , ''))

                if price_int < min_price: # and price_int >= 919500: # 26.10 filter >=919500
                # if price_int < min_price and price_int > num_check_for_outlier: - # temporarily turn off this filter 
                    sqm = row.find_all('td')[1].text.split()[0].strip()
                    min_price = price_int

        return min_price, sqm
    
    except:
        return '',''

def scrape_other_projects_nearby(soup):
    other_projects_nearby = None
    result = ''
    sections = soup.find_all('section')
    for section in sections:
        if section.find('h2', string='Other projects nearby'):
            other_projects_nearby = section.find('div', {'class': 'col-md-8'}).find_all('span')
            break
    
    if other_projects_nearby:
        for entry in other_projects_nearby:
            result += '{}; '.format(entry.text)
        result = result[:-2]
    
    return result

def scrape_popular_condos_in_area(soup):
    try:
        popular_condos_in_area = []
        popular_condos_in_area_block = soup.find('div', {'class': 'panel-body'}).find_all('div', {'class':'detail-block col-lg-8 left-block'})
        for condo in popular_condos_in_area_block:
            popular_condos_in_area.append(condo.find('h3').text.strip())
        result_str = ", ".join(popular_condos_in_area)
        return result_str
    except:
        return ''

def scrape_room_types_prices_ext(soup):
    result = []
    table_0 = soup.find('div', {'class':'container-table'})
    if table_0:
        table = table_0.find_all('div',{'class':'column text-center'})
        for row in table:
            row_dict = {}
            row_data_raw = row.find_all('div',{'class':'cell'})
            try:
                size = [int(s) for s in row_data_raw[1].text.split('m')[0].split() if s.isdigit()][0]
            except:
                size = ''
            try:
                number_of_units_for_rent = [int(s) for s in row_data_raw[2].text.split('For rent')[1].split('(')[1].split(')')[0].split() if s.isdigit()][0]
            except:
                number_of_units_for_rent = 0
            try:
                number_of_units_for_sale = [int(s) for s in row_data_raw[2].text.split('For sale')[1].split('(')[1].split(')')[0].split() if s.isdigit()][0]
            except:
                number_of_units_for_sale = 0
            try:
                average_rent = [int(s) for s in row_data_raw[2].text.replace(',','').split('For rent')[1].split('(')[0].split() if s.isdigit()][0]
            except:
                average_rent = ''
            try:
                average_ask_price = [int(s) for s in row_data_raw[2].text.replace(',','').split('For sale')[1].split('(')[0].split() if s.isdigit()][0]
            except:
                average_ask_price = ''

            row_dict.update({
                'size': size,
                'type': row_data_raw[0].text.strip(),
                'number of units for rent': number_of_units_for_rent,
                'number of units for sale': number_of_units_for_sale,
                'average rent': average_rent,
                'average ask price': average_ask_price
            })
            result.append(row_dict)
    
    print('---DEBUG---')
    print(result, len(result))
    return result

def get_data_graph(url):
    try:
        r = requests.get(url, headers=headers_xml, timeout=30)
        if r.status_code != 200:
            print('status_code', r.status_code)
            return None
        data = r.json()['msg']
        # print(data)
        
        try:
            median_rent_price_sqm = data.split("'sqmRent': {")[1].split("data:[")[1].split("],")[0].split(',')[-1]
        except:
            median_rent_price_sqm = ''
        try:
            earliest_median_rent_prices_sqm = data.split("'sqmRent': {")[1].split("data:[")[1].split("],")[0].split(',')
        except:
            earliest_median_rent_price_sqm = ''
        try:
            median_sale_price_sqm = data.split("'sqmSale': {")[1].split("data:[")[1].split("],")[0].split(',')[-1]
        except:
            median_sale_price_sqm = ''
        try:
            earliest_median_sale_prices_sqm = data.split("'sqmSale': {")[1].split("data:[")[1].split("],")[0].split(',')
        except:
            earliest_median_sale_prices_sqm = ''

        try:
            earliest_median_sale_price_sqm = ''
            if earliest_median_sale_prices_sqm == '':
                raise Exception
            month_num=0
            for price in earliest_median_sale_prices_sqm:
                month_num+=1
                if price!='':
                    earliest_median_sale_price_sqm = price
                    break
            
            months = data.split("labels: [")[1].split("],")[0].split(",")
            earliest_month = months[month_num-1].replace('"','')
        except:
            earliest_month = ''
        
        try:
            earliest_median_rent_price_sqm = ''
            if earliest_median_rent_prices_sqm == '':
                raise Exception
            month_num=0
            for price in earliest_median_rent_prices_sqm:
                month_num+=1
                if price!='':
                    earliest_median_rent_price_sqm = price
                    break
            
            months = data.split("labels: [")[1].split("],")[0].split(",")
            earliest_month_1 = months[month_num-1].replace('"','')
        except:
            earliest_month_1 = ''

        return median_rent_price_sqm, median_sale_price_sqm, earliest_median_sale_price_sqm, earliest_month, earliest_median_rent_price_sqm, earliest_month_1
    except requests.exceptions.RequestException as e:
        print(e)
        return '', '', '', '', '', ''

def get_data_projects(url):
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            print('status_code', r.status_code)
            return None
        soup = BeautifulSoup(r.content, 'html.parser')

        project_links = soup.find('div', {'id': 'search-results'}).find_all('a')
        result = set()
        for link in project_links:
            if link['href']:
                result.add(link['href'])
        print(result, len(result))
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def resolve_graph_link(url_project):
    if '/condo/' in url_project:
        id = url_project.split('/condo/')[1].split('/')[0]
        url = 'https://www.dotproperty.co.th/en/market-stats/project-page/condo/?key={}'.format(id)
        return url
    if '/showcase/' in url_project:
        id = url_project.split('/showcase/')[1].split('/')[0]
        url = 'https://www.dotproperty.co.th/en/market-stats/project-page/condo/?key={}'.format(id)
        return url

def check_outlier(num_or_spare, number_less, number_more=None):
    # (num_or_spare, digits_less, digits_more=None):
    # temporarily turn off the filter
    """
    if num_or_spare != '':
        if len(str(num_or_spare)) < digits_less:
            return ''
        if digits_more:
            if len(str(num_or_spare)) > digits_more:
                return ''
    """
    if num_or_spare != '':
        if int(num_or_spare) < number_less:
            return ''
        if number_more:
            if int(num_or_spare) > number_more:
                return ''
    return num_or_spare


if __name__ == "__main__":

    file_object = open('data/links_th_condo_thai_prov.json', 'r')
    links_thai_prov = json.load(file_object)
    file_object = open('data/links_th_condo_bk_dist.json', 'r')
    links_bk_dist = json.load(file_object)

    links = links_thai_prov + links_bk_dist
    result_1, result_2, result_3 = [], [], []
    
    j = 1
    for link in links:
        print(link, f"{j}/{len(links)}")
        result_bulk_1, result_bulk_2, result_bulk_3 = get_data_condo(link)
        if result_bulk_1:
            result_1.append(result_bulk_1)

            file_object = open('data/projects_data_th_condo_result_bulk_1.json', 'w')
            json.dump(result_1, file_object, indent=4)
        
        if result_bulk_2:
            result_2.append(result_bulk_2)

            file_object = open('data/projects_data_th_condo_result_bulk_2.json', 'w')
            json.dump(result_2, file_object, indent=4)
        
        if result_bulk_3:
            result_3.append(result_bulk_3)

            file_object = open('data/projects_data_th_condo_result_bulk_3.json', 'w')
            json.dump(result_3, file_object, indent=4)
        
        j += 1

        # graph_link = resolve_graph_link(link)
        # print(graph_link)
        # get_data_graph(graph_link)

        # time.sleep(1)
    
    # move it upper for write after each iteration
    # file_object = open('data/projects_data.json', 'w')
    # json.dump(result, file_object, indent=4)