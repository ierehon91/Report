import app.update.kapella as update_kapella
import app.update.pvd3 as update_pvd3
import app.update.gibrit as update_gibrit
import config

day = 14
month = 7
year = 2021

kapella = update_kapella.UpdateKapella(r'..\temp\kapella_data.csv', delimiter='$')
kapella_data = kapella.get_data(year, month, day)

pvd3 = update_pvd3.UpdatePvd3(config.pvd3_url)
pvd3.authorization(config.pvd3_username, config.pvd3_password)
pvd3.set_filial_number(config.pvd3_filial_number)
pvd3_data = pvd3.get_pvd_data(year, month, day)

gibrit = update_gibrit.UpdateGibrit(config.gibrit_url)
gibrit.authorization(config.gibrit_login, config.gibrit_password)
gibrit_data = gibrit.get_gibrit_data(year, month, day)
gibrit.close()

print(kapella_data)
print(pvd3_data)
print(gibrit_data)
