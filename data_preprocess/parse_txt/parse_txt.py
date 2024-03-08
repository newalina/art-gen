import csv


def retrieve_data(is_wiriting=False):
    file_path = 'HAQES_NA_v1.0_3h_PM25_BC_CENSUS.20240306.21z.txt'
    csv_file_path = 'pm2.5.csv'

    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # if line.startswith('===') or line.strip() == '':
            #     continue
            # if line.startswith('TRACT'):
            #     continue
            if not line.startswith('0'):
                continue 
            tract, pm25bc = line.split(',')
            data.append((tract.strip(), float(pm25bc.strip())))
            
    if is_wiriting:
        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['TRACT', 'pm25bc'])
            csvwriter.writerows(data)

        print('Data has been written to', csv_file_path)
        
    return data


def main():
    retrieve_data()
    return
    
if __name__ == '__main__':
    main()