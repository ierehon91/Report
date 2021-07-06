import app.update.kapella as update_kapella
import app.update.pvd3 as update_pvd3

day = 30
month = 6
year = 2021

pvd3_url = '10.36.35.13'
pvd3_username = 'i.merkulov',
pvd3_password = 'zmr00A'
pvd3_filial_number = 'MFC-000002595'

kapella = update_kapella.UpdateKapella(r'..\temp\kapella_data.csv', delimiter='$')
kapella_data = kapella.get_data(year, month, day)

pvd3 = update_pvd3.UpdatePvd3(pvd3_url, pvd3_username, pvd3_password)
pvd3.set_filial_number(pvd3_filial_number)
pvd3_data = pvd3.get_pvd_data(year, month, day)

print(kapella_data)
print(pvd3_data)
