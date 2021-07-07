import app.update.kapella as update_kapella
import app.update.pvd3 as update_pvd3
import app.update.gibrit as update_gibrit

day = 6
month = 7
year = 2021

pvd3_url = '10.36.35.13'
pvd3_username = 'i.merkulov',
pvd3_password = 'zmr00A'
pvd3_filial_number = 'MFC-000002595'

gibrit_login = 'sml-admin'
gibrit_password = '123456'
gibrit_url = '10.10.251.2:9000'

kapella = update_kapella.UpdateKapella(r'..\temp\kapella_data.csv', delimiter='$')
kapella_data = kapella.get_data(year, month, day)

# pvd3 = update_pvd3.UpdatePvd3(pvd3_url)
# pvd3.authorization(pvd3_username, pvd3_password)
# pvd3.set_filial_number(pvd3_filial_number)
# pvd3_data = pvd3.get_pvd_data(year, month, day)

# gibrit = update_gibrit.UpdateGibrit(gibrit_url)
# gibrit.authorization_gibrit(gibrit_login, gibrit_password)
# gibrit_data = gibrit.filial_gibrit_data(year, month, day, alias='Семилуки')
# gibrit.close()
#
print(kapella_data)
# print(pvd3_data)
# print(gibrit_data)
