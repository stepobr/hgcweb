# import os,sys
# import django


# # Set up Django settings module
# sys.path.append("/home/stepobr/CMS/box/db/hgcal_test/construct") 
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', '../hgcal_test.settings')
# django.setup()

# from construct.models import Parts,Cassettes

# with open('modulemapper_geometry.hgcal.txt', 'r') as file:
#     reader = csv.reader(file, delimiter=' ')
#     header = next(reader)  # skip header row
#     data = {}
#     for row in reader:
#         key = row[0]
#         values = row[1:]
#         data[key] = values
#         print (key)


# for name, values in data.items():
#     age = int(values[0])
#     gender = values[1]
#     person = Parts(name=name, age=age, gender=gender)
#     person.save()
import csv

# def read_csv_to_dict(filename):
#     data = []
#     with open(filename, 'r') as f:
#         reader = csv.reader(f, delimiter=' ')
#         headers = next(reader)  # Read the header row
#         for row in reader:
#             data.append(dict(zip(headers, row)))
#     return headers, data


# headers, data = read_csv_to_dict('modulemapper_geometry.hgcal.txt')
# for header in headers:
#     print(header)

