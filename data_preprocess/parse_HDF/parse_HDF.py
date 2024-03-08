'''
If you are having trouble download pyhdf using pip, consider conda:

conda create -n hdf4_env python=3.8
conda activate hdf4_env
conda install -c conda-forge pyhdf
'''

from pyhdf.SD import SD, SDC
import csv

def retrieve_data():
    file = SD('nasa.hdf', SDC.READ)
    datasets = file.datasets()
    datasets_info = []

    for name, info in datasets.items():
        # print("Name: ", name, " Info: ",info)
        datasets_info.append((name, info))

    # Replace 'dataset_name' with the actual name of your dataset
    # data_set = file.select('TotCldLiqH2O_MW_D')
    # data = data_set.get()
    # print(data)
    file.end()

    csv_file_path = 'datasets_info.csv'
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(['Dataset Name', 'Dimensions'])
        
        for name, info in datasets_info:
            # dimensions = info['shape']
            writer.writerow([name, info])
            

            
        
def main():
    file = SD('nasa.hdf', SDC.READ)
    datasets = file.datasets()
   
    # for name, info in datasets.items():
    #     print("Name: ", name, " Info: ",info)
    data_set = file.select('SurfSkinTemp_A')
    data = data_set.get()
    print(data)
    file.end()
    return 
        
if __name__ == '__main__':
    main()